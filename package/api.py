
import os, sys, shutil
sys.path.append(os.getcwd())

import requests
import pandas as pd
from colorama import init, Fore
from progress.bar import FillingSquaresBar
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill
from package.logo import version

import json

with open(os.path.join(os.getcwd(), 'config.json'), 'r', encoding='utf-8') as f:
    COMPANIES = json.load(f)['COMPANIES']

session = requests.Session()
session.keep_alive = False  # отключаем постоянные соединени
# ConnectionError(ProtocolError('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None)))

#API_KEY, COMPANY_ID, BANK_ACCOUNT_ID


def highlight_duplicate_idfromname(file_path) -> None:
    """
    Сканирует Excel-файл, находит строки с непустыми повторяющимися значениями
    в колонке 'idFromName' и заливает эти строки розовым цветом.

    :param file_path: путь к исходному .xlsx файлу
    :param sheet_name: имя листа (по умолчанию — активный лист)
    :param output_path: путь для сохранения (по умолчанию перезаписывает исходный)
    """
    # 1. Читаем данные, чтобы найти дубликаты
    df = pd.read_excel(file_path, dtype=str)
    if 'idFromName' not in df.columns:
        raise ValueError("В файле нет колонки 'idFromName'")

    # Нормализуем: пустые строки и NaN считаем пустыми
    col = df['idFromName'].fillna('').astype(str).str.strip()

    # Считаем количество вхождений каждого непустого значения
    counts = col[col != ''].value_counts()

    # Множество "плохих" значений (встречаются более одного раза)
    duplicates = set(counts[counts > 1].index)

    # Индексы строк (в терминах Excel: +2, т.к. строка 1 — заголовок, а df.index с 0)
    duplicate_row_indices = [
        i for i, val in enumerate(col) if val in duplicates
    ]

    # 2. Открываем книгу и закрашиваем
    wb = load_workbook(file_path)
    ws = wb.active

    pink_fill = PatternFill(start_color='FFC0CB', end_color='FFC0CB', fill_type='solid')

    # Определяем диапазон колонок по заголовку
    header = [cell.value for cell in ws[1]]
    last_col = len(header)

    for idx in duplicate_row_indices:
        excel_row = idx + 2  # +1 из-за заголовка, +1 из-за 1-based нумерации
        for col_idx in range(1, last_col + 1):
            ws.cell(row=excel_row, column=col_idx).fill = pink_fill

    # 3. Сохраняем
    wb.save(file_path)
    
    duplicate_row_indices_qty = len(duplicate_row_indices)
    if duplicate_row_indices_qty:
        print(Fore.RED + f"Внимание! Контрагентов с одинаковым сопоставленным оператором из весов: {duplicate_row_indices_qty/2}!")
    

def get_article_from_name(name):
    
    name_parts = str(name).split(' ')

    if len(name_parts) > 1:
        try:
            return int(name_parts[-1])
        except ValueError:
            return None 
    else:
        return None
             
    
    

def excel_formater(excel_file_path, column_widths, fill):
    wb = load_workbook(excel_file_path)
    ws = wb.active

    ws.freeze_panes = 'A2'

    for n, column_width in enumerate(column_widths, 1):
        ws.column_dimensions[get_column_letter(n)].width = column_width
        
        cell = ws.cell(row=1, column=n)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.fill = fill

    wb.save(excel_file_path)





def get_all_goods():
    
    dfs = []
    
    try:
        for COMPANY_INN, COMPANY_REQUISITES in COMPANIES.items():
            API_KEY = COMPANY_REQUISITES['API_KEY']
            COMPANY_ID = COMPANY_REQUISITES['COMPANY_ID']
            COMPANY_NAME = COMPANY_REQUISITES['COMPANY_NAME']
        
            if os.path.exists(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Номенклатура.xlsx')):
                os.remove(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Номенклатура.xlsx'))

            url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/products/search?"
            headers = {
                "X-Kontur-ApiKey": API_KEY,
                "Content-Type": "application/json",
                'Connection': 'close'
                }
            
            bar = FillingSquaresBar(
                f'Выгружаем ассортимент для {COMPANY_NAME}:',
                max=10,
                suffix = '%(index)d/%(max)d',
                fill='█', empty_fill='░',
                width = 50)  
            

            bar.start()
            for fig in range(0, 10):
                payload = {
                    "filter": {
                        "article": str(fig),                                              
                    }
                }

                response = session.post(url, headers=headers, json=payload)

                df = pd.DataFrame(response.json()['products'])

                df.insert(0, 'binded_company_name', COMPANY_NAME)
                df.insert(0, 'binded_company_inn', COMPANY_INN)
                dfs.append(df)
                
                bar.next()
                
            bar.finish()    
                
        goods_df = pd.concat(dfs, ignore_index=True)
        goods_df.drop_duplicates(inplace=True)
        goods_df = goods_df.sort_values('productMainName')


        goods_df.to_excel(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Номенклатура.xlsx'), index=None)

        excel_formater(
            os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Номенклатура.xlsx'),
            [20, 24, 38, 32, 8],
            PatternFill(fill_type='solid', fgColor='FFDDEBF7')
        )
    
        return (True, goods_df)
        
    except Exception as e:
            return (False, repr(e))
        

def get_all_contractors():
    
    try:
        dfs = []
            
        for COMPANY_INN, COMPANY_REQUISITES in COMPANIES.items():
            API_KEY = COMPANY_REQUISITES['API_KEY']
            COMPANY_ID = COMPANY_REQUISITES['COMPANY_ID']
            COMPANY_NAME = COMPANY_REQUISITES['COMPANY_NAME']
            
            if os.path.exists(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Контрагенты.xlsx')):
                os.remove(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Контрагенты.xlsx'))

            url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/contractors/search?"

            headers = {
                "X-Kontur-ApiKey": API_KEY,
                "Content-Type": "application/json",
                'Connection': 'close'
                }

            bar = FillingSquaresBar(
                f'Выгружаем контрагентов для {COMPANY_NAME}:',
                max=33,
                suffix = '%(index)d/%(max)d',
                fill='█', empty_fill='░',
                width = 50)  
            
            bar.start()
            
            for letter in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':

                payload = {
                    "filter": {
                        "name": letter,                                              
                    }
                }

                response = session.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    print(response.status_code)
                
                df = pd.DataFrame(response.json()['contractors'])
                df.insert(0, 'binded_company_name', COMPANY_NAME)
                df.insert(0, 'binded_company_id', COMPANY_ID)
                df.insert(0, 'binded_company_inn', COMPANY_INN)
                dfs.append(df)
                bar.next()
                
            bar.finish()    
                
        contractors_df = pd.concat(dfs, ignore_index=True)
        contractors_df.drop_duplicates(inplace=True)
        contractors_df = contractors_df.sort_values('name')
        contractors_df['idFromName'] = contractors_df['shortName'].apply(get_article_from_name)
        # contractors_df = contractors_df[['binded_company_inn', 'binded_company_name', 'id', 'name', 'shortName', 'idFromName', 'inn', 'kpp', 'address']]

        contractors_df.to_excel(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Контрагенты.xlsx'), index=None)

        excel_formater(
            os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Контрагенты.xlsx'),
            [20, 42, 24, 38, 42, 24, 12, 12, 12, 42],
            PatternFill(fill_type='solid',fgColor='FFC6EFCE')
        )
        
        highlight_duplicate_idfromname(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'Контрагенты.xlsx'))
            
        return (True, contractors_df)
        
    except Exception as e:
        return (False, repr(e))

def create_invoice(binded_company_inn, payload):
    # pprint(binded_company_inn)
    # pprint(payload)
    
    COMPANY_REQUISITES = COMPANIES[binded_company_inn]
    API_KEY = COMPANY_REQUISITES['API_KEY']
    COMPANY_ID = COMPANY_REQUISITES['COMPANY_ID']
    
    # url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/products/search?"
    url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/delivery-notes?"
    headers = {
        "X-Kontur-ApiKey": API_KEY,
        "Content-Type": "application/json",
        'Connection': 'close'
        }
    
    payload = payload
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 201:
        raise Exception(response.json())
        

    
"""
if __name__ == '__main__':
    payload = {
        "request": {},
        "bankAccountId": BANK_ACCOUNT_ID,
        "contractorId": "443a7b62-48ab-45a2-ba25-53adbf1edceb",
        "consigneeId": "443a7b62-48ab-45a2-ba25-53adbf1edceb",
        "date": "2026-05-31",
        'warehouseItems': [
            {'discount': None,
             'ndsRate': None,
             'price': 365,
             'productName': 'Лук зеленый',
             'quantity': 3.3,
             'unitName': 'кг'}]
    }
 
    create_invoice(payload)    
"""    

if __name__ == '__main__':
    highlight_duplicate_idfromname(os.path.join(r'C:\Users\DSTsv\invoice_creator_v.2026-11-21', 'Контрагенты.xlsx'))
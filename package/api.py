
import os, sys
sys.path.append(os.getcwd())

import requests
import pandas as pd
from colorama import init, Fore
from package.config import API_KEY, COMPANY_ID, BANK_ACCOUNT_ID
from progress.bar import FillingSquaresBar
from pprint import pprint
# --- НАСТРОЙКИ (замените на свои данные) ---
session = requests.Session()
session.keep_alive = False  # отключаем постоянные соединени
# ConnectionError(ProtocolError('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None)))
def get_all_goods():
    try:
        url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/products/search?"
        headers = {
            "X-Kontur-ApiKey": API_KEY,
            "Content-Type": "application/json"
            }
        dfs = []
        
        bar = FillingSquaresBar(
            ' Выгружаем ассортимент:',
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
            dfs.append(df)
            
            bar.next()
            
        bar.finish()    
            
        goods_df = pd.concat(dfs, ignore_index=True)
        goods_df.drop_duplicates(inplace=True)
        
        return (True, goods_df)
    
    except Exception as e:
        return (False, repr(e))

def get_all_contractors():
    
    try:
        url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/contractors/search?"

        headers = {
            "X-Kontur-ApiKey": API_KEY,
            "Content-Type": "application/json"
            }
        dfs = []
        
        bar = FillingSquaresBar(
            'Выгружаем контрагентов:',
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
            
            df = pd.DataFrame(response.json()['contractors'])
            dfs.append(df)
            bar.next()
            
        bar.finish()    
            
        goods_df = pd.concat(dfs, ignore_index=True)
        goods_df.drop_duplicates(inplace=True)
        
        return (True, goods_df)
    
    except Exception as e:
        return (False, repr(e))


def create_invoice(payload):
    
    # url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/products/search?"
    url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/delivery-notes?"
    headers = {
        "X-Kontur-ApiKey": API_KEY,
        "Content-Type": "application/json"
        }
    
    payload = payload
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 201:
        raise Exception(response.json())
        

    
    
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
    
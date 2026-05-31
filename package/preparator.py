import pandas as pd
import os,sys
sys.path.append(os.getcwd())

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

from package.sqlite import get_contractor_id, get_good_name

FONT_COLOR_GREEN = Font(color='2E8B57')
FONT_COLOR_RED = Font(color='FF0000')
LIGHT_BLUE_FILL = PatternFill(start_color='DDEBF7', 
                               end_color='DDEBF7', 
                               fill_type='solid')


def check_source_folder():
    source_files = list(os.walk('Исходник'))[0][2]
    source_files_qty = len(source_files)

    if source_files_qty!=1:
        return (False, f'В папке Исходник должен быть только один файл. Сейчас там: {source_files_qty}')
    elif source_files[0][-4:] != 'xlsx':
        return (False, 'В папке Исходник должен находится файл с расширением .xlsx')
    else:
        return (True, source_files[0])

def download_file_preparator(source_file_name):
    #try:
        
    if 1:
        invoices_qty = 0
        if os.path.exists(os.path.join(os.getcwd(), 'Для накладных.xlsx')):
            os.remove(os.path.join(os.getcwd(), 'Для накладных.xlsx'))
            
        wb = load_workbook(os.path.join(os.getcwd(), 'Исходник', source_file_name))
        ws = wb.active
        contractors_errors = 0
        goods_errors = 0
        

        for row_number in range(ws.max_row-1, 4, -1):
            row_cells = ws[row_number]
            row_values = [cell.value for cell in row_cells]
            #print(row_values)
            if row_values[3]=='Закрытие партии/чека':
                invoices_qty += 1
                for column_number in range(1, ws.max_column):
                    ws.cell(row=row_number, column=column_number).fill = LIGHT_BLUE_FILL
                
                contractor_id_res = get_contractor_id(row_values[18])
                if contractor_id_res[0]:
                    contractor_cell_color = FONT_COLOR_GREEN
                else:
                    contractors_errors += 1
                    contractor_cell_color = FONT_COLOR_RED
                contractor_cell_value = contractor_id_res[1]
            else:
                contractor_cell = ws.cell(row=row_number, column=19)
                contractor_cell.value = contractor_cell_value
                contractor_cell.font = contractor_cell_color
                
                productMainName_cell = ws.cell(row=row_number, column=6)
                get_good_name_res = get_good_name(row_values[4])
                
                if get_good_name_res[0]:
                    ws.cell(row=row_number, column=5).font = FONT_COLOR_GREEN
                    productMainName_cell.font = FONT_COLOR_GREEN
                else:
                    goods_errors += 1
                    ws.cell(row=row_number, column=5).font = FONT_COLOR_RED
                    productMainName_cell.font = FONT_COLOR_RED
                    
                productMainName_cell.value = get_good_name_res[1]
                
        
        err_message_cell = ws.cell(row=3, column=1)
        invoices_qty_cell = ws.cell(row=3, column=2)
        
        if contractors_errors or goods_errors:
            err_message = f"Не удалось определить конрагентов: {contractors_errors}; товаров: {goods_errors}"
            err_message_cell.font = FONT_COLOR_RED
            err_message_cell.value = err_message
            wb.save('Для накладных.xlsx')
            return (False, err_message)
        else:
            err_message_cell.font = FONT_COLOR_GREEN
            err_message_cell.value = 'Накладных:'
            
            invoices_qty_cell.font = FONT_COLOR_GREEN
            invoices_qty_cell.value = invoices_qty
            
            wb.save('Для накладных.xlsx')
            return (True, 'Файл "Для накладных.xlsx" подготовлен. Ошибок нет.')
    
    #except Exception as e:
    #    return(False, f"download_file_preparator {repr(e)}")

    
if __name__ == '__main__':
    print(download_file_preparator('29.05.26 без ошибок.xlsx'))

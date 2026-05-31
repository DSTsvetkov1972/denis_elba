from datetime import datetime
import os, shutil
from openpyxl import load_workbook

def confirm():
    try:
        wb= load_workbook(os.path.join(os.getcwd(), 'Для накладных.xlsx'))
        ws = wb.active
        if ws.cell(column=1, row=3).value != 'Накладных:':
            return (False, 'Файл "Для накладных.xlsx" содержит ошибки')
        
        source_file_name = list(os.walk(os.path.join(os.getcwd(), 'Исходник')))[0][2][0]
        source_file_path = os.path.join(os.getcwd(), 'Исходник', source_file_name)
        
        archive_file_name = f"{str(datetime.now())[:19].replace(':', '-')}_{source_file_name}"
        archive_file_path = os.path.join(os.getcwd(), 'Архив', archive_file_name)
        
        shutil.move(os.path.join(os.getcwd(), 'Для накладных.xlsx'), archive_file_path)
        os.remove(source_file_path)
        
        return (True, 'Файл перемещен в архив {archive_file_name}')
    except Exception as e:
        return (False, repr(e))
    
if __name__ == '__main__':
    confirm()
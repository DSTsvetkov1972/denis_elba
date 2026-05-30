import pandas as pd
import os


def check_source_folder():
    source_files = list(os.walk('Исходник'))[0][2]
    source_files_qty = len(source_files)

    if source_files_qty!=1:
        return (False, f'В папке Исходник должен быть только один файл. Сейчас там: {source_files_qty}')
    elif source_files[0][-4:] != 'xlsx':
        return (False, 'В папке Исходник должен находится файл с расширением .xlsx')
    else:
        return (True,)

def get_source_file_parts():
    source_file = list(os.walk('Исходник'))[0][2][0]
    source_file_path = os.path.join('Исходник', source_file)

    df = pd.read_excel(source_file_path, header=3)
    print(df.columns)
    df['Контрагент'] = df.apply(lambda x: None if x['Операция']!='Закрытие партии/чека' else x['Контрагент'], axis=1)


    #df = df[['Операция', 'ID товара', 'Контрагент']]
    
    
    df_splitter = df[df['Операция']=='Закрытие партии/чека']
    df_splitter_errs = df_splitter[df['Контрагент']=='']
    
    if not df_splitter_errs.empty:
        splitter_errs_rows = [row+5 for row in df_splitter_errs.index.to_list()]
        return (False, f'Не заполнен контрагент в строках исходника: {splitter_errs_rows}')
    
    df['Контрагент'] = df['Контрагент'].bfill()

    df = df[df['Операция']=='Продажа']
    
    return(df)
if __name__ == '__main__':
    df =get_source_file_parts()
    df.to_excel('aaa.xlsx')
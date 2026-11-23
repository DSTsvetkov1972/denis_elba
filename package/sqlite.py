import pandas as pd
import sqlite3
import os, sys

sys.path.insert(0, os.getcwd())
from package.logo import version
# Подключаемся к БД (создастся автоматически)



def df_to_sqlite(df, table_name):
    with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        
def get_contractor_id(name, operation):
    try:
        if operation in ['Закрытие смены', 'Аварийное закрытие партии']:
            return(True, operation)
        
        with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
            sql_res = pd.read_sql_query(f"SELECT * FROM contractors WHERE name='{name}' AND idFromName IS NOT NULL AND idFromName<>''", conn)
            
            if not sql_res.empty:
                return(True, sql_res['id'].iloc[0])
            else:
                return (False, f'Контрагент "{name}" не найден или не сопоставлен компании')
    except Exception as e:
        return(False, f'get_contractor_id: {repr(e)}')
            

def get_info_from_idFromName(idFromName):
    try:
        with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
            sql_res = pd.read_sql_query(f"SELECT * FROM contractors WHERE idFromName='{idFromName}'", conn)

            if sql_res.empty:
                return (False, f'Код оператора {idFromName} не сопоставлен с контрагентом')
            
            if len(sql_res)>1:
                return (False, f'Код оператора {idFromName} сопоставлен нескольким контрагентам')
    
            return(
                True,
                {'name': sql_res['name'].iloc[0],
                'binded_company_name': sql_res['binded_company_name'].iloc[0],
                'binded_company_inn': sql_res['binded_company_inn'].iloc[0],
                'binded_company_id': sql_res['binded_company_id'].iloc[0]}
                )

    except Exception as e:
        return(False, f'get_contractor_name_from_idFromName: {repr(e)}')
    


def get_good_name(article, binded_company_name):
    try:
        with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
            sql_res = pd.read_sql_query(f"SELECT * FROM goods WHERE article='{article}' AND binded_company_name='{binded_company_name}'", conn)
            # print(sql_res)
            
            if sql_res.empty:
                return (False, f'Товар с артикулом "{article}" не найден у компании "{binded_company_name}"')
            
            if len(sql_res)>1:
                return (False, f'У {binded_company_name} товаров с артикулом {article}: {len(sql_res)}')
            
            if not sql_res.empty:
                return(True, sql_res['productMainName'].iloc[0])

    except Exception as e:
        return(False, f'get_contractor_id: {repr(e)}')
   
if __name__ == '__main__':
    print(get_good_name(None, 'ИП Собольков Д. С.'))

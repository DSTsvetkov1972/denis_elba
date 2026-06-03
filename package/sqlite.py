import pandas as pd
import sqlite3
import os
# Подключаемся к БД (создастся автоматически)



def df_to_sqlite(df, table_name):
    with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)


def get_product(article):
    with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
        result = pd.read_sql_query(f"SELECT * FROM products WHERE articule={article}", conn)
        print(result)

def get_contractor_id(name, operation):
    try:
        if operation in ['Закрытие смены', 'Аварийное закрытие партии']:
            return(True, operation)
        
        with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
            sql_res = pd.read_sql_query(f"SELECT * FROM contractors WHERE name='{name}'", conn)
            
            if not sql_res.empty:
                return(True, sql_res['id'].iloc[0])
            else:
                return (False, f'Контрагент "{name}" не найден')
    except Exception as e:
        return(False, f'get_contractor_id: {repr(e)}')
    

def get_good_name(article):
    try:
        with sqlite3.connect(os.path.join(os.getcwd(), 'app.db')) as conn:
            sql_res = pd.read_sql_query(f"SELECT * FROM goods WHERE article='{article}'", conn)
            
            if not sql_res.empty:
                return(True, sql_res['productMainName'].iloc[0])
            else:
                return (False, f'Товар с артикулом "{article}" не найден')
    except Exception as e:
        return(False, f'get_contractor_id: {repr(e)}')
   
if __name__ == '__main__':
    print(get_good_name('222'))
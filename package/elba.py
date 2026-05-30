import requests
import pandas as pd
from colorama import init, Fore
from config import API_KEY, COMPANY_ID
from progress.bar import FillingSquaresBar

# --- НАСТРОЙКИ (замените на свои данные) ---


def get_all_goods():
    url = f"https://elba-api.kontur.ru/v1/organizations/{COMPANY_ID}/products/search?"
    headers = {
        "X-Kontur-ApiKey": API_KEY,
        "Content-Type": "application/json"
        }
    dfs = []
    
    bar = FillingSquaresBar(
        'Выгружаем ассортимент:',
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

        response = requests.post(url, headers=headers, json=payload)

        df = pd.DataFrame(response.json()['products'])
        dfs.append(df)
        
        bar.next()
        
    bar.finish()    
        
    goods_df = pd.concat(dfs, ignore_index=True)
    goods_df.drop_duplicates(inplace=True)
    
    return goods_df

def get_all_contractors():
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

        response = requests.post(url, headers=headers, json=payload)
        
        df = pd.DataFrame(response.json()['contractors'])
        dfs.append(df)
        bar.next()
        
    bar.finish()    
        
    goods_df = pd.concat(dfs, ignore_index=True)
    goods_df.drop_duplicates(inplace=True)
    
    return goods_df

if __name__ == '__main__':
    print(get_all_contractors())
    
    
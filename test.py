import requests
import pandas as pd
from colorama import init, Fore

# --- НАСТРОЙКИ (замените на свои данные) ---

API_KEY = "b79404c9-798f-40c3-bab0-3a99c63278d1"
COMPANY_ID = "3775a938-d183-4c49-887c-1b14ec0e262a"
# Эндпоинт для получения списка документов или информации о компании
# Запрос к компаниям часто требует меньше всего прав для проверки
url = f"https://elba-api.kontur.ru/v1/organizations/3775a938-d183-4c49-887c-1b14ec0e262a/products/search?"
#url = f"https://elba-api.kontur.ru/v1/organizations/3775a938-d183-4c49-887c-1b14ec0e262a/products/search?"

headers = {
    "X-Kontur-ApiKey": API_KEY,
    "Content-Type": "application/json"
    }




payload = {
    "filter": {
        "productName": "Тыква кругл."
        #"article": "4"
    }
}



response = requests.post(url, headers=headers, json=payload)


df = pd.DataFrame(response.json()['products'])

print(int(df['article'].iloc[0]))
#print(df)


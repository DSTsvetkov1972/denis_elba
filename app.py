import requests

# --- НАСТРОЙКИ (замените на свои данные) ---
API_KEY = "b79404c9-798f-40c3-bab0-3a99c63278d1"
COMPANY_ID = "3775a938-d183-4c49-887c-1b14ec0e262a"

# Эндпоинт для получения списка документов или информации о компании
# Запрос к компаниям часто требует меньше всего прав для проверки
url = f"https://elba-api.kontur.ru/v1/organizations/3775a938-d183-4c49-887c-1b14ec0e262a/products/search?"
#url = f"https://elba-api.kontur.ru/v1/organizations?"

headers = {
    "X-Kontur-ApiKey": API_KEY,
    "Content-Type": "application/json"
    }

payload = {
    "offset": 10,
    "limit": 50,
}

# ------------------------------------------

def check_connection():
    response = requests.post(url, headers=headers, json=payload)
        
    print(response.status_code)
    

    print(response.json())


if __name__ == "__main__":
    check_connection()
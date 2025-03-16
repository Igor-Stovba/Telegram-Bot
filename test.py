import requests
import config

IAM_TOKEN = config.YANDEX_IAM_TOKEN
CATALOG_ID = config.YANDEX_CATALOG_ID
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

headers = {
    "Authorization": f"Bearer {IAM_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "modelUri": f"gpt://{CATALOG_ID}/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.5,
        "maxTokens": 150
    },
    "messages": [
        {"role": "user", "text": "Привет! Как дела?"}
    ]
}

response = requests.post(GPT_URL, headers=headers, json=data)

if response.status_code == 200:
    print(response.json())  # Выведет ответ модели
else:
    print(f"Ошибка {response.status_code}: {response.text}")  # Покажет ошибку

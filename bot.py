import logging
import requests
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

# 🔑 Ваши ключи
TELEGRAM_BOT_TOKEN = "---"  # Замените на ваш токен бота
YANDEX_API_KEY = "---"  # Замените на ваш API-ключ Yandex

# Логирование
logging.basicConfig(level=logging.INFO)

# 🧠 Функция для работы с Yandex GPT
def get_gpt_response(prompt):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": "gpt://---/yandexgpt-lite",
        "messages": [{"role": "user", "text": prompt}],
        "temperature": 0.7,
        "maxTokens": 500,
        "topP": 1
    }

    # Отправка запроса к Yandex GPT
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            logging.info(f"Ответ от Yandex GPT: {result}")  # Логируем полный ответ
            # Извлекаем текст из структуры ответа
            if "result" in result and "alternatives" in result["result"]:
                return result["result"]["alternatives"][0]["message"]["text"]
            else:
                return "Не удалось обработать ответ Yandex GPT. Проверьте структуру ответа."
        except Exception as e:
            logging.error(f"Ошибка обработки ответа от Yandex GPT: {e}")
            return "Произошла ошибка при обработке ответа от Yandex GPT."
    else:
        logging.error(f"Ошибка Yandex GPT: {response.status_code} - {response.text}")
        return "Произошла ошибка при обращении к Yandex GPT 😔"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Обработчик сообщений
@router.message()
async def handle_message(message: Message):
    user_input = message.text.strip()  # Удаляем лишние пробелы
    if not user_input:  # Проверяем, пустое ли сообщение
        await message.answer("Сообщение не может быть пустым. Попробуйте снова!")
        return

    await message.answer("🤖 Думаю над ответом...")
    try:
        response = get_gpt_response(user_input)  # Запрашиваем ответ у Yandex GPT
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения 😥")

# Подключение роутера
dp.include_router(router)

# Запуск бота
async def main():
    logging.info("Бот запущен 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

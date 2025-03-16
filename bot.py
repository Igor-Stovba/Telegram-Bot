import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import config
from quiz import QuizManager
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
quiz_manager = QuizManager()

config_yandex_gpt = {
    "model_type": "yandex_gpt",
    "catalog_id": config.YANDEX_CATALOG_ID,
    "iam_token": config.YANDEX_IAM_TOKEN
}

config = YandexGPTConfigManagerForAPIKey(model_type=config.YANDEX_MODEL_TYPE, 
                                         catalog_id=config.YANDEX_CATALOG_ID, 
                                         api_key=config.YANDEX_IAM_TOKEN)
yandex_gpt = YandexGPT(config_manager=config)

# # Инициализируем БД
# init_db()

def get_gpt_response(prompt: str) -> str:
    messages = [{"role": "user", "text": prompt}]
    completion = yandex_gpt.get_sync_completion(messages=messages, 
                                                temperature=0.5,
                                                max_tokens=150)
    return completion

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Напиши 'TEST' для начала теста или задай мне вопрос.")

@bot.message_handler(func=lambda message: message.text.strip().upper() == "TEST")
def start_quiz(message):
    user_id = message.from_user.id
    quiz_manager.start_quiz(user_id)
    send_next_question(message)

def send_next_question(message):
    user_id = message.from_user.id
    question_data = quiz_manager.get_next_question(user_id)

    if question_data:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [KeyboardButton(str(i+1)) for i in range(4)]
        markup.add(*buttons)

        bot.send_message(message.chat.id, question_data["question"], reply_markup=markup)
    else:

        bot.send_message(message.chat.id, "Тест завершен! Спасибо за участие.")


@bot.message_handler(func=lambda message: message.text in ["1", "2", "3", "4"])
def handle_answer(message):
    user_id = message.from_user.id
    quiz_manager.process_answer(user_id, message.text)

    is_end = quiz_manager.is_end_of_test(user_id)
    if is_end is None:
        bot.send_message(message.chat.id, f"Тест завершен! Ваш результат: {quiz_manager.get_final_result(user_id)}")
    else:
        send_next_question(message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # this method is for AI Agent
    user_input = message.text
    bot.send_chat_action(message.chat.id, "typing")
    response_text = get_gpt_response(user_input)
    bot.send_message(message.chat.id, response_text)


if __name__ == "__main__":
    bot.polling(none_stop=True)

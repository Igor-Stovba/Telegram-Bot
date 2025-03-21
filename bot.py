import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import config
from quiz import QuizManager

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
quiz_manager = QuizManager()

# # Инициализируем БД
# init_db()

def get_gpt_response(prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {config.YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "text": "Ты — эксперт в области психологии. Отвечай только на вопросы, связанные с психологией и моральной поддержкой. Если вопрос выходит за рамки темы, отвечай: 'Я отвечаю только на вопросы по мотивационной и психологической тематике.'"},
        {"role": "user", "text": prompt}
    ]
    data = {
        "modelUri": config.MODEL_URI,
        "messages": messages,
        "temperature": 0.7,
        "maxTokens": 500,
        "topP": 1
    }

    # Отправка запроса к Yandex GPT
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            if "result" in result and "alternatives" in result["result"]:
                return result["result"]["alternatives"][0]["message"]["text"]
            else:
                return "Не удалось обработать ответ Yandex GPT. Проверьте структуру ответа."
        except Exception as e:
            return "Произошла ошибка при обработке ответа от Yandex GPT."
    else:
        return "Произошла ошибка при обращении к Yandex GPT 😔"
    

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
        rt, lt = quiz_manager.get_final_result(user_id)
        bot.send_message(message.chat.id, "Твой результат:")
        bot.send_message(message.chat.id, f"Реактивная тревожность: {rt}")
        bot.send_message(message.chat.id, f"Личностная тревожность: {lt}")
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

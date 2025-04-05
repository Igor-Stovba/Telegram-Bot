import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import config
from quiz import QuizManager
from database import TaskManager

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
quiz_manager = QuizManager()
task_manager = TaskManager()    

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Напиши 'TEST' для начала теста или задай мне вопрос.")

@bot.message_handler(func=lambda message: message.text.strip().upper() == "TEST")
def start_quiz(message):
    user_id = message.from_user.id
    quiz_manager.start_quiz(user_id)
    bot.send_message(message.chat.id, "1 - Нет, 2 - Скорее нет, 3 - Скорее да, 4 - Да")
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

# Логика по CRUD task

@bot.message_handler(commands=["addtask"])
def add_task_handler(message):
    bot.send_message(message.chat.id, "Введите описание задачи:")
    bot.register_next_step_handler(message, get_task_description)

def get_task_description(message):
    user_id = message.from_user.id
    description = message.text
    bot.send_message(message.chat.id, "Введите дедлайн задачи (в формате YYYY-MM-DD) или напишите 'нет'):")
    bot.register_next_step_handler(message, lambda msg: get_task_deadline(msg, user_id, description))

def get_task_deadline(message, user_id, description):
    deadline = message.text if message.text.lower() != "нет" else None
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Важно", "Не важно")
    bot.send_message(message.chat.id, "Задача важная?", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: get_task_importance(msg, user_id, description, deadline))

def get_task_importance(message, user_id, description, deadline):
    important = message.text == "Важно"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Срочно", "Не срочно")
    bot.send_message(message.chat.id, "Задача срочная?", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: get_task_urgency(msg, user_id, description, deadline, important))

def get_task_urgency(message, user_id, description, deadline, important):
    urgent = message.text == "Срочно"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Нет")
    bot.send_message(message.chat.id, "Уведомлять о дедлайне?", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: save_task(msg, user_id, description, deadline, important, urgent))

def save_task(message, user_id, description, deadline, important, urgent):
    notify = message.text == "Да"
    task_manager.add_task(user_id, description, deadline, important, urgent, notify)
    bot.send_message(message.chat.id, "Задача добавлена!")

@bot.message_handler(commands=["tasks"])
def list_tasks_handler(message):
    user_id = message.from_user.id
    tasks = task_manager.get_tasks(user_id)
    if not tasks:
        bot.send_message(message.chat.id, "У вас нет задач.")
    else:
        for task in tasks:
            status = "✅ Выполнено" if task["completed"] else "❌ Не выполнено"
            bot.send_message(message.chat.id, f"{task['id']}: {task['description']}\nДедлайн: {task['deadline']}\n{status}")

@bot.message_handler(commands=["done"])
def complete_task_handler(message):
    bot.send_message(message.chat.id, "Введите ID задачи, которую хотите отметить выполненной:")
    bot.register_next_step_handler(message, mark_task_completed)

def mark_task_completed(message):
    try:
        task_id = int(message.text)
        task_manager.mark_task_completed(task_id)
        bot.send_message(message.chat.id, "Задача отмечена как выполненная!")
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректный ID задачи.")

@bot.message_handler(commands=["delete"])
def delete_task_handler(message):
    bot.send_message(message.chat.id, "Введите ID задачи, которую хотите удалить:")
    bot.register_next_step_handler(message, delete_task)

def delete_task(message):
    try:
        task_id = int(message.text)
        task_manager.delete_task(task_id)
        bot.send_message(message.chat.id, "Задача удалена!")
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректный ID задачи.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # this method is for AI Agent
    user_input = message.text
    bot.send_chat_action(message.chat.id, "typing")
    response_text = get_gpt_response(user_input)
    bot.send_message(message.chat.id, response_text)

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

if __name__ == "__main__":
    bot.polling(none_stop=True)

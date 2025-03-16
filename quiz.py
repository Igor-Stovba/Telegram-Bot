import random

QUESTIONS = [
    {"question": "Я спокоен", "options": ["1", "2", "3", "4"]},
    {"question": "Мне ничто не угрожает", "options": ["1", "2", "3", "4"]},
    {"question": "Я нахожусь в напряжении", "options": ["1", "2", "3", "4"]},
    {"question": "Я испытываю сожаление", "options": ["1", "2", "3", "4"]},
    {"question": "Я чувствую себя свободно", "options": ["1", "2", "3", "4"]},
    {"question": "Я расстроен", "options": ["1", "2", "3", "4"]},
    {"question": "Меня волнуют возможные неудачи", "options": ["1", "2", "3", "4"]},
    {"question": "Я чувствую себя отдохнувшим", "options": ["1", "2", "3", "4"]},
    {"question": "Я не доволен собой", "options": ["1", "2", "3", "4"]},
    {"question": "Я испытываю чувство внутреннего удовлетворения", "options": ["1", "2", "3", "4"]},
    {"question": "Я уверен в себе", "options": ["1", "2", "3", "4"]},
    {"question": "Я нервничаю", "options": ["1", "2", "3", "4"]},
    {"question": "Я не нахожу себе места", "options": ["1", "2", "3", "4"]},
    {"question": "Я взвинчен", "options": ["1", "2", "3", "4"]},
    {"question": "Я не чувствую скованности, напряженности", "options": ["1", "2", "3", "4"]},
    {"question": "Я доволен", "options": ["1", "2", "3", "4"]},
    {"question": "Я озабочен", "options": ["1", "2", "3", "4"]},
    {"question": "Я слишком возбужден, и мне не по себе", "options": ["1", "2", "3", "4"]},
    {"question": "Мне радостно", "options": ["1", "2", "3", "4"]},
    {"question": "Мне приятно", "options": ["1", "2", "3", "4"]},
    {"question": "Я испытываю удовольствие", "options": ["1", "2", "3", "4"]},
    {"question": "Я очень быстро устаю", "options": ["1", "2", "3", "4"]},
    {"question": "Я легко могу заплакать", "options": ["1", "2", "3", "4"]},
    {"question": "Я хотел бы быть таким же счастливым, как и другие", "options": ["1", "2", "3", "4"]},
    {"question": "Нередко я проигрываю из-за того, что недостаточно быстро принимаю решения", "options": ["1", "2", "3", "4"]},
    {"question": "Обычно я чувствую себя бодрым", "options": ["1", "2", "3", "4"]},
    {"question": "Я спокоен, хладнокровен и собран", "options": ["1", "2", "3", "4"]},
    {"question": "Ожидаемые трудности обычно очень тревожат меня", "options": ["1", "2", "3", "4"]},
    {"question": "Я слишком переживаю из-за пустяков", "options": ["1", "2", "3", "4"]},
    {"question": "Я вполне счастлив", "options": ["1", "2", "3", "4"]},
    {"question": "Я принимаю все слишком близко к сердцу", "options": ["1", "2", "3", "4"]},
    {"question": "Мне не хватает уверенности в себе", "options": ["1", "2", "3", "4"]},
    {"question": "Обычно я чувствую себя в безопасности", "options": ["1", "2", "3", "4"]},
    {"question": "Я стараюсь избегать критических ситуаций", "options": ["1", "2", "3", "4"]},
    {"question": "У меня бывает хандра", "options": ["1", "2", "3", "4"]},
    {"question": "Я доволен", "options": ["1", "2", "3", "4"]},
    {"question": "Всякие пустяки отвлекают и волнуют меня", "options": ["1", "2", "3", "4"]},
    {"question": "Я так сильно переживаю свои разочарования, что потом долго не могу о них забыть", "options": ["1", "2", "3", "4"]},
    {"question": "Я уравновешенный человек", "options": ["1", "2", "3", "4"]},
    {"question": "Меня охватывает сильное беспокойство, когда я думаю о своих делах и заботах", "options": ["1", "2", "3", "4"]}
]

class QuizManager:
    def __init__(self):
        self.active_quizzes = {}

    def start_quiz(self, user_id):
        random.shuffle(QUESTIONS)
        self.active_quizzes[user_id] = {"questions": QUESTIONS.copy(), "score": 0, "current": 0}

    def get_next_question(self, user_id):
        quiz = self.active_quizzes.get(user_id)
        if quiz and quiz["current"] < len(quiz["questions"]):
            return quiz["questions"][quiz["current"]]
        return None
    
    def is_end_of_test(self, user_id):
        quiz = self.active_quizzes.get(user_id)
        if quiz and quiz["current"] < len(quiz["questions"]):
            return False
        return True

    def process_answer(self, user_id, answer_index):
        quiz = self.active_quizzes.get(user_id)
        if not quiz:
            return None
        
        # Dummy, todo
        quiz["score"] += 1

        quiz["current"] += 1
    
    def get_final_result(self, user_id):
        final_score = 22 # Dummy
        if (final_score > 22):
            return "Bad result"
        else:
            return "Good result"
        

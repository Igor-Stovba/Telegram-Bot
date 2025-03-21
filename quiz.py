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

RT_SCALE_1 = {3, 4, 6, 7, 9, 12, 13, 14, 17, 18}
RT_SCALE_2 = {1, 2, 5, 8, 10, 11, 15, 16, 19, 20}
LT_SCALE_1 = {22, 23, 24, 25, 28, 29, 31, 32, 34, 35, 37, 38, 40}
LT_SCALE_2 = {21, 26, 27, 30, 33, 36, 39}

class QuizManager:
    def __init__(self):
        self.active_quizzes = {}

    def start_quiz(self, user_id):
        random.shuffle(QUESTIONS)
        self.active_quizzes[user_id] = {"questions": QUESTIONS.copy(), "answers": {}, "current": 0}

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
    
    def process_answer(self, user_id, answer):
        quiz = self.active_quizzes.get(user_id)
        if not quiz:
            return None
        
        question_index = quiz["current"] + 1
        quiz["answers"][question_index] = int(answer) 
        quiz["current"] += 1

    def calculate_scores(self, user_id):
        quiz = self.active_quizzes.get(user_id)
        if not quiz:
            return None

        answers = quiz["answers"]
        
        RT_1 = sum(answers[q] for q in RT_SCALE_1 if q in answers)
        RT_2 = sum(answers[q] for q in RT_SCALE_2 if q in answers)
        RT = RT_1 - RT_2 + 35

        LT_1 = sum(answers[q] for q in LT_SCALE_1 if q in answers)
        LT_2 = sum(answers[q] for q in LT_SCALE_2 if q in answers)
        LT = LT_1 - LT_2 + 35
        
        return RT, LT
    
    def interpret_score(self, score):
        if score <= 30:
            return "Низкий уровень!"
        elif 31 <= score <= 45:
            return "Умеренный уровень!"
        else:
            return "Высокий уровень!"
    
    def get_final_result(self, user_id):
        RT, LT = self.calculate_scores(user_id)
        return self.interpret_score(RT), self.interpret_score(LT)

        

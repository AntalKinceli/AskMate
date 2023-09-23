""" Bussiness logic layer """

from datetime import datetime
# import connection

questions = []


def show_questions(reverse=False):
    return reversed(questions) if reverse else questions


def submit_question(title, message):
    question = {'title': title, 'message': message, 'edit_count': 0}

    question['id'] = max((item['id']
                         for item in questions)) + 1 if questions else 1

    question['submission_time'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    questions.append(question)

    return question['id']


def question_by_id(id):
    return [q for q in questions if q['id'] == id][0]

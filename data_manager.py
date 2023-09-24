""" Bussiness logic layer """

from datetime import datetime
import connection


def show_questions(reverse=False):
    questions = connection.load_question()

    return reversed(questions) if reverse else questions


def submit_question(title, message):
    questions = connection.load_question()

    question = {'title': title, 'message': message, 'view_number': -1}
    # view number will be 0 after the redirect
    question['id'] = max((int(item['id'])
                         for item in questions)) + 1 if questions else 1
    question['submission_time'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    questions.append(question)
    connection.write_question(questions)

    return question['id']


def question_by_id(id):
    questions = connection.load_question()

    question = [q for q in questions if int(q['id']) == id][0]
    question['view_number'] = int(question['view_number']) + 1

    connection.write_question(questions)

    return question

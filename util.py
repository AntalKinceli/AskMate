""" Utility funcitons for data_manager """

from datetime import datetime
import connection


def question_io(func):
    def func_wrapper(*args, **kwargs):
        questions = connection.load_question()
        return_value = func(questions, *args, **kwargs)
        connection.write_question(questions)

        return return_value

    return func_wrapper


def answer_io(func):
    def func_wrapper(*args, **kwargs):
        answers = connection.load_answers()
        return_value = func(answers, *args, **kwargs)
        connection.write_answers(answers)

        return return_value

    return func_wrapper


def question_by_id(questions, id):
    for question in questions:
        if question['id'] == id:
            return question


def entry_position(dataset, id):
    for n, data in enumerate(dataset):
        if data['id'] == id:
            return n


def submission_time():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

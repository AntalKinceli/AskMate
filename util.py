""" Utility funcitons for data_manager """

from datetime import datetime


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

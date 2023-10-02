""" Data connection layer """

import csv

QUESTIONS_FILE = 'data/question.csv'
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'title',
                    'message', 'vote_number', 'picture']


def load_questions():
    try:
        with open(QUESTIONS_FILE, newline='') as file:
            return list(csv.DictReader(file, fieldnames=QUESTIONS_HEADER))
    except FileNotFoundError:
        print('CSV file not found.')


def write_questions(data):
    with open(QUESTIONS_FILE, 'w') as file:
        csv.DictWriter(file, fieldnames=QUESTIONS_HEADER).writerows(data)


ANSWERS_FILE = 'data/answer.csv'
ANSWERS_HEADER = ['id', 'submission_time',
                  'question_id', 'title', 'message', 'vote_number']


def load_answers():
    try:
        with open(ANSWERS_FILE, newline='') as file:
            return list(csv.DictReader(file, fieldnames=ANSWERS_HEADER))
    except FileNotFoundError:
        print('CSV file not found.')


def write_answers(data):
    with open(ANSWERS_FILE, 'w') as file:
        csv.DictWriter(file, fieldnames=ANSWERS_HEADER).writerows(data)

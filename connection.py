""" Data connection layer """

import csv

QUESTIONS_FILE = 'data/question.csv'
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'title', 'message']


def load_question():
    try:
        with open(QUESTIONS_FILE, newline='') as file:
            return list(csv.DictReader(file, fieldnames=QUESTIONS_HEADER))
    except FileNotFoundError:
        print('CSV file not found.')


def write_question(data):
    with open(QUESTIONS_FILE, 'w') as file:
        csv.DictWriter(file, fieldnames=QUESTIONS_HEADER).writerows(data)

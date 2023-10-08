""" Data connection layer """

import csv
import os
import psycopg2
import psycopg2.extras

""" CSS backup """

QUESTIONS_FILE = 'data/question.csv'
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'title',
                    'message', 'vote_number', 'image']


def load_questions():
    try:
        with open(QUESTIONS_FILE, newline='') as file:
            return list(csv.DictReader(file, fieldnames=QUESTIONS_HEADER))
    except FileNotFoundError:
        print('CSV file not found.')


# def write_questions(data):
#     with open(QUESTIONS_FILE, 'w') as file:
#         csv.DictWriter(file, fieldnames=QUESTIONS_HEADER).writerows(data)


ANSWERS_FILE = 'data/answer.csv'
ANSWERS_HEADER = ['id', 'submission_time',
                  'question_id', 'title', 'message', 'vote_number']


def load_answers():
    try:
        with open(ANSWERS_FILE, newline='') as file:
            return list(csv.DictReader(file, fieldnames=ANSWERS_HEADER))
    except FileNotFoundError:
        print('CSV file not found.')


# def write_answers(data):
#     with open(ANSWERS_FILE, 'w') as file:
#         csv.DictWriter(file, fieldnames=ANSWERS_HEADER).writerows(data)


""" Postgresql operational storage """
""" DB connection identifiers are loaded from os system variables,
    which are set during the venv initialisation from bin/activate script. """


def get_connection_string():
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    db = os.environ.get('PSQL_DB_NAME')

    if user_name and password and host and db:
        return fr"postgresql://{user_name}:{password}@{host}/{db}"
    else:
        raise KeyError('Some SQL enviroment variale(s) are missing')


def connection_handler(func):
    def wrapper(*args, **kwargs):
        try:
            connection = psycopg2.connect(get_connection_string())
            connection.autocommit = True
        except psycopg2.DatabaseError as exception:
            print('Database connection failed')
            raise exception

        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        return_value = func(cursor, *args, **kwargs)

        cursor.close()
        connection.close()
        return return_value

    return wrapper

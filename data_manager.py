""" Bussiness logic layer """

import connection
import util
# from psycopg2 import sql


def load_data():
    global questions
    questions = connection.load_questions()
    global answers
    answers = connection.load_answers()


""" Questions """


def show_questions(order_column, reverse):
    return sorted(questions, key=lambda x: x[order_column], reverse=reverse)


def question_by_id(id, increment_views=False):
    question = util.entry_by_id(questions, id)
    if increment_views:
        question['view_number'] = str(int(question['view_number']) + 1)

    return question


def submit_question(title, message, imported_file):
    question = {'title': title, 'message': message,
                'view_number': 0, 'vote_number': 0}
    question['id'] = str(max((int(item['id'])
                         for item in questions)) + 1 if questions else 1)
    question['submission_time'] = util.submission_time()
    if imported_file:
        question['picture'] = util.upload_file(imported_file)
    else:
        question['picture'] = ''

    questions.append(question)
    connection.write_questions(questions)
    return question['id']


def edit_question(id, title, message, imported_file):
    question = util.entry_by_id(questions, id)

    question['title'] = title
    question['message'] = message
    if imported_file:
        question['picture'] = util.upload_file(
            imported_file, question['picture'])

    connection.write_questions(questions)


def delete_question(id):
    questions.pop(util.entry_position(questions, id))

    connection.write_questions(questions)
    delete_answers_to_question(id)


def delete_answers_to_question(question_id):
    # instead of delete create a new list without the deleted answers
    updated_answers = [a for a in answers if a['question_id'] != question_id]

    connection.write_answers(updated_answers)


def vote_question(question_id, upvote):
    question = util.entry_by_id(questions, question_id)

    if upvote:
        question['vote_number'] = str(int(question['vote_number']) + 1)
    else:
        question['vote_number'] = str(int(question['vote_number']) - 1)

    connection.write_questions(questions)


""" Answers """


def submit_answer(question_id, title, message):
    answer = {'title': title, 'message': message,
              'question_id': question_id, 'vote_number': 0}
    answer['id'] = str(max((int(item['id'])
                            for item in answers)) + 1 if answers else 1)
    answer['submission_time'] = util.submission_time()

    answers.append(answer)
    connection.write_answers(answers)


def answers_by_question_id(question_id):
    return [a for a in answers if a['question_id'] == question_id]


def delete_answer(answer_id):
    answer = answers.pop(util.entry_position(answers, answer_id))

    connection.write_answers(answers)
    return answer['question_id']


def vote_answer(answer_id, upvote):
    answer = util.entry_by_id(answers, answer_id)

    if upvote:
        answer['vote_number'] = str(int(answer['vote_number']) + 1)
    else:
        answer['vote_number'] = str(int(answer['vote_number']) - 1)

    connection.write_answers(answers)
    return answer['question_id']

# @connection_handler
# def init_db(cursor):
#     # removing the test table if it already exists
#     cursor.execute("DROP TABLE IF EXISTS test;")
#     cursor.execute(
#         "CREATE TABLE test (id serial PRIMARY KEY,"
#         + " num integer, data varchar);")

#     # Psycopg perform the correct execution (no more SQL injections!)
#     cursor.execute(
#         "INSERT INTO test (num, data) VALUES (%s, %s)",
#         (100, "First row"))
#     cursor.execute(
#         "INSERT INTO test (num, data) VALUES (%s, %s)",
#         (200, "Second row"))


# @connection_handler
# def fetch_db_example(cursor):
#     # query the database and obtain data as Python objects
#     userinput = 'data'
#     cursor.execute(sql.SQL("SELECT num, {} FROM test;").format(
#         sql.Identifier(userinput)))
#     rows = cursor.fetchall()
#     print(rows)

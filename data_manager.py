""" Bussiness logic layer """

import connection as conn
from psycopg2 import sql
import util


""" Questions """


@conn.connection_handler
def show_questions(cursor, order_column, reverse):
    query_str = """SELECT id, submission_time, title, message,
                    view_number, vote_number, image
                    FROM question
                    ORDER BY {}""" + ('DESC' if reverse else 'ASC')

    cursor.execute(sql.SQL(query_str).format(sql.Identifier(order_column)))
    return cursor.fetchall()


@conn.connection_handler
def submit_question(cursor, title, message, imported_file):
    if imported_file:
        image_name = util.upload_file(imported_file)
    else:
        image_name = ''

    query = sql.SQL("""INSERT INTO question (submission_time, view_number,
                       vote_number, title, message, image)
                       VALUES (%s, %s, %s, {fields})
                        RETURNING id""").format(
        fields=sql.SQL(',').join([
            sql.Literal(title),
            sql.Literal(message),
            sql.Literal(image_name)]))

    cursor.execute(query, (util.submission_time(), 0, 0))
    return cursor.fetchone()['id']


@conn.connection_handler
def question_by_id(cursor, id):
    query = sql.SQL("""UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = {}
                    RETURNING *""").format(sql.Literal(int(id)))

    cursor.execute(query)
    return dict(cursor.fetchone())


# def edit_question(id, title, message, imported_file):
#     question = util.entry_by_id(questions, id)

#     question['title'] = title
#     question['message'] = message
#     if imported_file:
#         question['picture'] = util.upload_file(
#             imported_file, question['picture'])

#     conn.write_questions(questions)


# def delete_question(id):
#     questions.pop(util.entry_position(questions, id))

#     conn.write_questions(questions)
#     delete_answers_to_question(id)


# def delete_answers_to_question(question_id):
#     # instead of delete create a new list without the deleted answers
#     updated_answers = [a for a in answers if a['question_id'] != question_id]

#     conn.write_answers(updated_answers)


# def vote_question(question_id, upvote):
#     question = util.entry_by_id(questions, question_id)

#     if upvote:
#         question['vote_number'] = str(int(question['vote_number']) + 1)
#     else:
#         question['vote_number'] = str(int(question['vote_number']) - 1)

#     conn.write_questions(questions)


""" Answers """


# def submit_answer(question_id, title, message):
#     answer = {'title': title, 'message': message,
#               'question_id': question_id, 'vote_number': 0}
#     answer['id'] = str(max((int(item['id'])
#                             for item in answers)) + 1 if answers else 1)
#     answer['submission_time'] = util.submission_time()

#     answers.append(answer)
#     conn.write_answers(answers)

@conn.connection_handler
def answers_by_question_id(cursor, question_id):
    query = sql.SQL("""SELECT * FROM answer
                    WHERE {} = question_id""").format(
        sql.Literal(int(question_id)))

    cursor.execute(query)

    return cursor.fetchall()

# def delete_answer(answer_id):
#     answer = answers.pop(util.entry_position(answers, answer_id))

#     conn.write_answers(answers)
#     return answer['question_id']


# def vote_answer(answer_id, upvote):
#     answer = util.entry_by_id(answers, answer_id)

#     if upvote:
#         answer['vote_number'] = str(int(answer['vote_number']) + 1)
#     else:
#         answer['vote_number'] = str(int(answer['vote_number']) - 1)

#     conn.write_answers(answers)
#     return answer['question_id']

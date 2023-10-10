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


@conn.connection_handler
def edit_question(cursor, id, title, message, imported_file):
    query = sql.SQL("""SELECT image FROM question
                    WHERE id = {}""").format(
        sql.Literal(int(id)))
    cursor.execute(query)

    if imported_file:
        filename = util.upload_file(imported_file, cursor.fetchone()['image'])
    else:
        filename = cursor.fetchone()['image']

    query = sql.SQL("""UPDATE question
                    SET title = {title}, message = {message}, image = {image}
                    WHERE id = {id}""").format(
        title=sql.Literal(title),
        message=sql.Literal(message),
        image=sql.Literal(filename),
        id=sql.Literal(int(id)))

    cursor.execute(query)


@conn.connection_handler
def delete_question(cursor, id):
    query = sql.SQL("""DELETE FROM question
                    WHERE id = {}""").format(
        sql.Literal(int(id)))

    cursor.execute(query)


@conn.connection_handler
def vote_question(cursor, question_id, upvote):
    query = sql.SQL("""UPDATE question
                    SET vote_number = vote_number + %s
                    WHERE id = {}""").format(
        sql.Literal(int(question_id)))

    cursor.execute(query, (1 if upvote else -1,))


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

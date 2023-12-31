""" Bussiness logic layer """

import connection as conn
from psycopg2 import sql
import util

""" Search """


@conn.connection_handler
def search(cursor, search_text):
    literal = sql.Literal('%' + search_text + '%')
    query = sql.SQL("""SELECT DISTINCT id, submission_time,
                    view_number, vote_number, title,
                    message, image
                    FROM question
                    WHERE title ILIKE {} OR message ILIKE {}
                    ORDER BY id""").format(
        literal, literal)
    cursor.execute(query)

    # fancy search
    results = []
    for real_dict_row in cursor.fetchall():
        row = dict(real_dict_row)

        splitted = row['title'].split(search_text)
        row['title'] = ('<span>' + search_text + '</span>').join(splitted)
        splitted = row['message'].split(search_text)
        row['message'] = ('<span>' + search_text + '</span>').join(splitted)

        results.append(row)

    return results


""" Questions """


@conn.connection_handler
def show_questions(cursor, order_column='id', reverse=True, limit=None):
    query_str = """SELECT * FROM question
                    ORDER BY {}""" + ('DESC' if reverse else 'ASC') \
        + (f' LIMIT {limit}' if limit else '')
    query = sql.SQL(query_str).format(sql.Identifier(order_column))

    cursor.execute(query)
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


@conn.connection_handler
def submit_answer(cursor, question_id, message):
    query = sql.SQL("""INSERT INTO answer (submission_time,
                       vote_number, question_id, message)
                       VALUES (%s, %s, {fields})
                        RETURNING id""").format(
        fields=sql.SQL(',').join([
            sql.Literal(int(question_id)),
            sql.Literal(message)]))

    cursor.execute(query, (util.submission_time(), 0))
    return cursor.fetchone()['id']


@conn.connection_handler
def edit_answer(cursor, id, message):
    query = sql.SQL("""UPDATE answer
                    SET message = {message}
                    WHERE id = {id}""").format(
        message=sql.Literal(message),
        id=sql.Literal(int(id)))

    cursor.execute(query)


@conn.connection_handler
def answer_by_id(cursor, id):
    query = sql.SQL("""SELECT * FROM answer
                WHERE id = {}""").format(sql.Literal(int(id)))

    cursor.execute(query)
    return dict(cursor.fetchone())


@conn.connection_handler
def delete_answer(cursor, answer_id):
    query = sql.SQL("""DELETE FROM answer
                    WHERE id = {}
                    RETURNING question_id""").format(
        sql.Literal(int(answer_id)))

    cursor.execute(query)
    return cursor.fetchone()['question_id']


@conn.connection_handler
def answers_by_question_id(cursor, question_id):
    query = sql.SQL("""SELECT * FROM answer
                    WHERE {} = question_id
                    ORDER BY id""").format(
        sql.Literal(int(question_id)))

    cursor.execute(query)
    return cursor.fetchall()


@conn.connection_handler
def vote_answer(cursor, answer_id, upvote):
    query = sql.SQL("""UPDATE answer
                    SET vote_number = vote_number + %s
                    WHERE id = {}
                    RETURNING question_id""").format(
        sql.Literal(int(answer_id)))

    cursor.execute(query, (1 if upvote else -1,))
    return cursor.fetchone()['question_id']


""" Comments """


@conn.connection_handler
def submit_comment_to_question(cursor, question_id, message):
    query = sql.SQL("""INSERT INTO comment (submission_time,
                       question_id, message)
                       VALUES (%s, {fields})
                        RETURNING id""").format(
        fields=sql.SQL(',').join([
            sql.Literal(int(question_id)),
            sql.Literal(message)]))

    cursor.execute(query, (util.submission_time(),))


@conn.connection_handler
def comments_by_question_id(cursor, question_id):
    query = sql.SQL("""SELECT * FROM comment
                    WHERE {} = question_id
                    ORDER BY id""").format(
        sql.Literal(int(question_id)))

    cursor.execute(query)
    return cursor.fetchall()


@conn.connection_handler
def submit_comment_to_answer(cursor, answer_id, message):
    query = sql.SQL("""INSERT INTO comment (submission_time,
                       answer_id, message)
                       VALUES (%s, {fields})
                        RETURNING id""").format(
        fields=sql.SQL(',').join([
            sql.Literal(int(answer_id)),
            sql.Literal(message)]))

    cursor.execute(query, (util.submission_time(),))


@conn.connection_handler
def question_id_by_answer_id(cursor, id):
    query = sql.SQL("""SELECT question_id FROM answer
                WHERE id = {}""").format(sql.Literal(int(id)))

    cursor.execute(query)
    return dict(cursor.fetchone())['question_id']


@conn.connection_handler
def comments_by_answers(cursor, answers):
    answer_ids = tuple(answer['id'] for answer in answers)
    query = sql.SQL("""SELECT * FROM comment
                    WHERE answer_id IN %s""")

    cursor.execute(query, (answer_ids,))
    return cursor.fetchall()


@conn.connection_handler
def comment_by_id(cursor, id):
    query = sql.SQL("""SELECT * FROM comment
                WHERE id = {}""").format(sql.Literal(int(id)))

    cursor.execute(query)
    return dict(cursor.fetchone())


@conn.connection_handler
def edit_comment(cursor, id, message):
    query = sql.SQL("""UPDATE comment
                    SET message = {message}
                    WHERE id = {id}""").format(
        message=sql.Literal(message),
        id=sql.Literal(int(id)))

    cursor.execute(query)


@conn.connection_handler
def delete_comment(cursor, comment_id):
    query = sql.SQL("""DELETE FROM comment
                    WHERE id = {}""").format(
        sql.Literal(int(comment_id)))

    cursor.execute(query)


@conn.connection_handler
def question_id_by_comment_id(cursor, id):
    query = sql.SQL("""SELECT question.id
                FROM question
                FULL JOIN comment ON question.id = question_id
                WHERE comment.id = {}""").format(sql.Literal(int(id)))

    cursor.execute(query)
    question_comment = dict(cursor.fetchone())['id']

    query = sql.SQL("""SELECT question.id
                    FROM question
                    FULL JOIN answer ON question.id = question_id
                    FULL JOIN comment ON answer.id = answer_id
                    WHERE comment.id = {}""").format(sql.Literal(int(id)))

    cursor.execute(query)
    answer_comment = dict(cursor.fetchone())['id']

    return question_comment if question_comment else answer_comment

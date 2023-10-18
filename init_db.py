import connection as conn


@conn.connection_handler
def init_db(cursor):
    # build schema
    cursor.execute("DROP TABLE IF EXISTS question CASCADE;")
    cursor.execute("""CREATE TABLE question (
                   id serial PRIMARY KEY,
                   submission_time timestamp,
                   view_number int,
                   vote_number int,
                   title varchar,
                   message varchar,
                   image varchar);""")

    cursor.execute("DROP TABLE IF EXISTS answer CASCADE;")
    cursor.execute("""CREATE TABLE answer (
                   id serial PRIMARY KEY,
                   submission_time timestamp,
                   vote_number int,
                   question_id int REFERENCES question ON DELETE CASCADE,
                   message varchar)""")

    cursor.execute("DROP TABLE IF EXISTS comment CASCADE;")
    cursor.execute("""CREATE TABLE comment (
                   id serial PRIMARY KEY,
                   submission_time timestamp,
                   question_id int REFERENCES question ON DELETE CASCADE,
                   answer_id int REFERENCES answer ON DELETE CASCADE,
                   message varchar)""")

    # load sample data
    for question in conn.load_questions():
        cursor.execute("""INSERT INTO question (submission_time, view_number,
                       vote_number, title, message, image)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                       (question['submission_time'], question['view_number'],
                        question['vote_number'], question['title'],
                        question['message'], question['image']))

    for answer in conn.load_answers():
        cursor.execute("""INSERT INTO answer (submission_time, vote_number,
                       question_id, message)
                       VALUES (%s, %s, %s, %s)""",
                       (answer['submission_time'], answer['vote_number'],
                        answer['question_id'], answer['message']))

    for comment in conn.load_comments():
        cursor.execute("""INSERT INTO comment (submission_time,
                       question_id, answer_id, message)
                       VALUES (%s, %s, %s, %s)""",
                       (comment['submission_time'],
                        (comment['question_id'] if comment['question_id']
                        != 'NULL' else None),
                        (comment['answer_id'] if comment['answer_id']
                        != 'NULL' else None),
                        comment['message']))
        # psycopg2 uses None as null value, but pgadmin4 exports it
        # as NULL due to SQL standard

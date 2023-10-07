import connection as conn


def load_data():
    global questions
    questions = conn.load_questions()
    global answers
    answers = conn.load_answers()


@conn.connection_handler
def init_db(cursor):
    # build schema
    cursor.execute("DROP TABLE IF EXISTS question CASCADE;")
    cursor.execute("""CREATE TABLE question (
                   id serial PRIMARY KEY,
                   submission_time date,
                   view_number int,
                   vote_number int,
                   title varchar,
                   message varchar,
                   image varchar);""")

    cursor.execute("DROP TABLE IF EXISTS answer CASCADE;")
    cursor.execute("""CREATE TABLE answer (
                   id serial PRIMARY KEY,
                   submission_time date,
                   vote_number int,
                   question_id int REFERENCES question,
                   message varchar,
                   image varchar)""")
    # load data
    # cursor.execute("""INSERT INTO question (num, data) VALUES (%s, %s)""",
    #                (100, "First row"))

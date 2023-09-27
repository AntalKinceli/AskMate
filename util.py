""" Utiliy funcitons for data_manager """

import connection


def question_io(func):
    def func_wrapper(*args, **kwargs):
        questions = connection.load_question()
        return_value = func(questions, *args, **kwargs)
        connection.write_question(questions)

        return return_value

    return func_wrapper


def entry_by_id(dataset, id):
    return [q for q in dataset if int(q['id']) == id][0]

""" Bussiness logic layer """

import connection
import util


def show_questions(order_column, reverse):
    questions = connection.load_question()

    response = sorted(
        questions, key=lambda x: x[order_column], reverse=reverse)

    return response


@util.question_io
def question_by_id(questions, id, increment_views=False):
    question = util.question_by_id(questions, id)
    if increment_views:
        question['view_number'] = str(int(question['view_number']) + 1)

    return question


@util.question_io
def submit_question(questions, title, message):
    question = {'title': title, 'message': message, 'view_number': 0}
    question['id'] = str(max((int(item['id'])
                         for item in questions)) + 1 if questions else 1)
    question['submission_time'] = util.submission_time()

    questions.append(question)

    return question['id']


@util.question_io
def edit_question(questions, id, title, message):
    question = util.question_by_id(questions, id)

    question['title'] = title
    question['message'] = message


@util.question_io
def delete_question(questions, id):
    questions.pop(util.entry_position(questions, id))

    delete_answers_to_question(id)


def delete_answers_to_question(question_id):
    answers = connection.load_answers()

    # instead of delete create a new list without the deleted answers
    answers = [a for a in answers if int(a['question_id']) != question_id]

    connection.write_answers(answers)


@util.answer_io
def submit_answer(answers, question_id, title, message):
    answer = {'title': title, 'message': message, 'question_id': question_id}
    answer['id'] = str(max((int(item['id'])
                            for item in answers)) + 1 if answers else 1)
    answer['submission_time'] = util.submission_time()

    answers.append(answer)


@util.answer_io
def answers_by_question_id(answers, question_id):
    return [a for a in answers if a['question_id'] == question_id]


@util.answer_io
def delete_answer(answers, answer_id):
    answer = answers.pop(util.entry_position(answers, answer_id))

    return answer['question_id']

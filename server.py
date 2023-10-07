""" Routing layer - main entry """

from flask import Flask, render_template, redirect, request, url_for
import data_manager as dm
from init_db import init_db

app = Flask(__name__)

QUESTIONS_WEB_HEADER = {'ID': 'id', 'Time': 'submission_time',
                        'Title': 'title', 'Question': 'message',
                        'Views': 'view_number', 'Votes': 'vote_number'}
ANSWERS_WEB_HEADER = {'ID': 'question_id', 'Time': 'submission_time',
                      'Title': 'title', 'Answer': 'message',
                      'Votes': 'vote_number'}


@app.route('/')
@app.route('/list')
def index():

    column = QUESTIONS_WEB_HEADER['ID']
    reverse = True

    if request.args:
        column = QUESTIONS_WEB_HEADER[request.args.get('order_by')]
        reverse = request.args.get('order_direction') == 'desc'

    return render_template('index.html', header=QUESTIONS_WEB_HEADER.keys(),
                           questions=dm.show_questions(column, reverse))


""" Questions """


@app.route('/question/<question_id>')
def display_question(question_id):
    question = dm.question_by_id(question_id, increment_views=True)
    answers = dm.answers_by_question_id(question_id)

    return render_template('question.html', header=ANSWERS_WEB_HEADER.keys(),
                           question=question, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = dm.submit_question(request.form.get('title'),
                                request.form.get('message'),
                                request.files['picture'])

        return redirect(url_for('display_question', question_id=id))

    return render_template('ask.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        dm.edit_question(question_id, request.form.get('title'),
                         request.form.get('message'),
                         request.files['picture'])

        return redirect(url_for('display_question', question_id=question_id))

    question = dm.question_by_id(question_id)

    return render_template('edit.html', question=question)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    dm.delete_question(question_id)

    return redirect(url_for('index'))


@app.route('/question/<question_id>/vote_up')
def question_vote_up(question_id):
    dm.vote_question(question_id, upvote=True)

    return redirect(url_for('index'))


@app.route('/question/<question_id>/vote_down')
def question_vote_down(question_id):
    dm.vote_question(question_id, upvote=False)

    return redirect(url_for('index'))


""" Answers """


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        dm.submit_answer(question_id, request.form.get('title'),
                         request.form.get('message'))

        return redirect(url_for('display_question', question_id=question_id))

    return render_template('answer.html', question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    return redirect(url_for('display_question',
                            question_id=dm.delete_answer(answer_id)))


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    question_id = dm.vote_answer(answer_id, upvote=True)

    return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    question_id = dm.vote_answer(answer_id, upvote=False)

    return redirect(url_for('display_question', question_id=question_id))


if __name__ == '__main__':
    init_db()

    app.run(debug=True)

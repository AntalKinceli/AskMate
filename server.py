""" Routing layer - main entry """

from flask import Flask, render_template, redirect, request, url_for
import data_manager as dm

app = Flask(__name__)
HEADER = {'ID': 'id', 'Time': 'submission_time', 'Title': 'title',
          'Question': 'message', 'Views': 'view_number'}


@app.route('/')
@app.route('/list')
def index():

    column = HEADER['ID']
    reverse = True

    if request.args:
        column = HEADER[request.args.get('order_by')]
        reverse = request.args.get('order_direction') == 'desc'

    return render_template('index.html', header=HEADER.keys(),
                           questions=dm.show_questions(column, reverse))


@app.route('/question/<int:question_id>')
def display_question(question_id):

    return render_template('question.html',
                           question=dm.question_by_id(question_id,
                                                      increment_views=True))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = dm.submit_question(request.form.get('title'),
                                request.form.get('message'))

        return redirect(url_for('display_question', question_id=id))

    return render_template('ask.html')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        dm.edit_question(question_id, request.form.get('title'),
                         request.form.get('message'))

        return redirect(url_for('display_question', question_id=question_id))

    question = dm.question_by_id(question_id)

    return render_template('edit.html', question=question)


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):

    dm.delete_question(question_id)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

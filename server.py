""" Routing layer - main entry """

from flask import Flask, render_template, redirect, request
import data_manager as dm

app = Flask(__name__)
HEADER = ['ID', 'Time', 'Title', 'Question', 'Edits']


@app.route('/')
@app.route('/list')
def index():

    return render_template('index.html', header=HEADER,
                           questions=dm.show_questions(reverse=True))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = dm.submit_question(request.form.get('title'),
                                request.form.get('message'))

        return redirect(f'/question/{id}')

    return render_template('ask.html')


@app.route('/question/<int:question_id>')
def display_question(question_id):

    return render_template('question.html',
                           question=dm.question_by_id(question_id))


if __name__ == '__main__':
    app.run(debug=True)

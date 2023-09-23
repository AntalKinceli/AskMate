""" Routing layer - main entry """
from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():

    return render_template('index.html', header=HEADER,
                           questions=reversed(questions))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = {}

        if questions:
            question['id'] = max((item['id'] for item in questions)) + 1
        else:
            question['id'] = 1
        question['title'] = request.form.get('title')
        question['message'] = request.form.get('message')
        question['edit_count'] = 0

        questions.append(question)

        return redirect(f'/question/{question["id"]}')

    return render_template('ask.html')


@app.route('/question/<int:question_id>')
def display_question(question_id):
    question = [q for q in questions if q['id'] == question_id][0]

    return render_template('question.html', question=question)


if __name__ == '__main__':
    app.run(debug=True)

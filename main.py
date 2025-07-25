
from flask import Flask, render_template
import json
import os
import requests
import random
app = Flask(__name__)

questions = {
    1:'Advanced-Math.json',
    2:'Algebra.json',
    3:'Craft-and-Structure.json',
    4:"Expression-of-Ideas.json",
    5:'Geometry-and-Trigonometry.json',
    6:'Information-and-Ideas.json',
    7:'Problem-Solving-and-Data-Analysis.json',
    8:'Standard-English-Conventions.json'

}
def load_data(which):
    # Takes 1-8 as input and returns the corresponding data file


    DATA_FILE = os.path.join(os.path.dirname(__file__), 'questions', questions[which])

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/practice')
def pratice():
    data = load_data(random.randint(1, 8))
    if not data:
        return render_template('pratice.html', error="No questions found.")
    random_question_index = random.randint(0, len(data) - 1)
    payload = {"external_id": data[random_question_index]['external_id']}
    test_cat = data[random_question_index]['general_area'].split('/')
    domain = data[random_question_index]['problem_area']
    difficulty = data[random_question_index]['difficulty']
    response = requests.post(
        'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
        json=payload)
    question = response.json()
    return render_template('pratice.html', data=question, cat=test_cat, domain=domain, difficulty=difficulty)

if __name__ == '__main__':
    app.run(debug=True)

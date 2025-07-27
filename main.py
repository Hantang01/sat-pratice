from flask import send_from_directory
# Serve static files from 'media' folder

from flask import send_from_directory, Flask, render_template, jsonify, request
import json
import os
import requests
import random
from dotenv import load_dotenv
from helpers.binary_decoder import decode
load_dotenv()
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
desmos_api_key = os.getenv('DESMOS_API_KEY')

catagory = [
    # English
    "Cross-Text Connections",
    "Text Structure and Purpose",
    "Words in Context",
    "Rhetorical Synthesis",
    "Transitions",
    "Central Ideas and Details",
    "Command of Evidence",
    "Inferences",
    "Boundaries",
    "Form, Structure, and Sense",
    # Math
    "Linear equations in one variable",
    "Linear functions",
    "Linear equations in two variables",
    "Systems of two linear equations in two variables",
    "Linear inequalities in one or two variables",
    "Equivalent expressions",
    "Nonlinear equations in one variable and systems of equations in two variables",
    "Nonlinear functions",
    "Ratios, rates, proportional relationships, and units",
    "Percentages",
    "One-variable data: Distributions and measures of center and spread",
    "Two-variable data: Models and scatterplots",
    "Probability and conditional probability",
    "Inference from sample statistics and margin of error",
    "Evaluating statistical claims: Observational studies and experiments",
    "Area and volume",
    "Lines, angles, and triangles",
    "Right triangles and trigonometry",
    "Circles"
]
def load_data(which):
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

@app.route('/practices', methods=['GET', 'POST'])
def practice():
    # List all subject IDs in order
    subject_ids = [
        'Percentages', 'Ratios, rates, proportional relationships, and units', 'One-variable data: Distributions and measures of center and spread', 'Evaluating statistical claims: Observational studies and experiments',
    ]
    binary_code = None
    if request.method == 'POST':
        selected = request.form.get('subjects')
        binary_code = ''.join(['1' if sid in selected else '0' for sid in subject_ids])
    return render_template('practice.html')


@app.route('/pratices/suite/<encoded>')
def practice_suite(encoded):
   # Invalid encoded value 
    if int(encoded) > 536870911:
       return render_template('404.html'), 404
    to_be_tested = decode(encoded)
    return render_template('question-pratice.html', categories=to_be_tested)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('media', filename)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/random-practice')
def random_practice():
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
    return render_template('random_pratice.html', data=question, cat=test_cat, domain=domain, difficulty=difficulty, desmos_api_key=desmos_api_key)

@app.route('/api/random-question')
def api_random_question():
    data = load_data(random.randint(1, 8))
    if not data:
        return jsonify({"error": "No questions found."}), 404
    random_question_index = random.randint(0, len(data) - 1)
    payload = {"external_id": data[random_question_index]['external_id']}
    test_cat = data[random_question_index]['general_area'].split('/')
    domain = data[random_question_index]['problem_area']
    difficulty = data[random_question_index]['difficulty']
    response = requests.post(
        'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
        json=payload)
    question = response.json()
    question['cat'] = test_cat
    question['domain'] = domain
    question['difficulty'] = difficulty
    return jsonify(question)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
 


from flask import send_from_directory
# Serve static files from 'media' folder
import os
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
    1:'Advanced-Math',
    2:'Algebra.json',
    3:'Craft-and-Structure',
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
    # data = load_data(random.randint(1, 8))
    # if not data:
    #     return render_template('pratice.html', error="No questions found.")
    # random_question_index = random.randint(0, len(data) - 1)
    # payload = {"external_id": data[random_question_index]['external_id']}
    # test_cat = data[random_question_index]['general_area'].split('/')
    # domain = data[random_question_index]['problem_area']
    # difficulty = data[random_question_index]['difficulty']
    # response = requests.post(
    #     'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
    #     json=payload)
    # question = response.json()
    all_files = os.listdir('./question_data')

    random_test_type = random.choice([f for f in all_files])


    random_category = random.choice([f for f in os.listdir(f'./question_data/{random_test_type}')])
    random_difficulty = random.choice(['Easy', 'Medium', 'Hard'])

    file_name = random_test_type + "_"+ random_category + "_" + random_difficulty + ".json"


    full_path = f'./question_data/{random_test_type}/{random_category}/{file_name}'

    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        random_question = random.choice(data)
        
        # Try standard format first
        if "answerOptions" in random_question and "stem" in random_question:
            pass  # Already in standard format

        # Try alternative 'fore' format
        elif "answer" in random_question and "prompt" in random_question:
            # Convert fore format to standard format
            if "choices" in random_question["answer"]:
                choices = random_question["answer"]["choices"]
                answerOptions = []
                for key in sorted(choices.keys()):
                    answerOptions.append({
                        "content": choices[key]["body"],
                        "id": key
                    })
            else:
                answerOptions = []
            
            correct = random_question["answer"].get("correct_choice", "")
            if isinstance(correct, str):
                correct = [correct.upper()]
            elif isinstance(correct, list):
                correct = [c.upper() for c in correct]
            else:
                correct = []

            random_question = {
                "stimulus": "",
                "stem": random_question.get("prompt", ""),
                "answerOptions": answerOptions,
                "correct_answer": correct,
                "rationale": random_question["answer"].get("rationale", ""),
                "difficulty": random_question.get("difficulty", random_difficulty),
                "skill_desc": random_question.get("skill_desc", random_question.get("skill", "")),
                "primary_class_cd_desc": random_question.get("primary_class_cd_desc", ""),
            }

        # If neither format, use what we have
        else:
            # Ensure we have the required fields for the template
            if "stem" not in random_question:
                random_question["stem"] = random_question.get("prompt", "Question format not recognized.")
            if "answerOptions" not in random_question:
                random_question["answerOptions"] = []
            if "correct_answer" not in random_question:
                random_question["correct_answer"] = []
            if "rationale" not in random_question:
                random_question["rationale"] = ""

    if random_category in ['EOI', 'INI', 'SEC', 'CAS']:
        test_cat = "English"
    else:
        test_cat = "Math"

    try:
        difficulty = random_question['difficulty']
    except:
        difficulty = random_difficulty + "?"
        
    sat_category_map = {
        "P": "Advanced-Math",
        "INI": "Information-and-Ideas",
        "SEC": "Standard-English-Conventions",
        "CAS": "Craft-and-Structure",
        "Q": "Problem-Solving-and-Data-Analysis",
        "EOI": "Expression-of-Ideas",
        "S": "Geometry-and-Trigonometry",
        "H": "Algebra"
    }
    domain = sat_category_map.get(random_category, random_category)
    skill = random_question.get('skill_desc', random_question.get('skill', 'Unknown'))


    return render_template('random_pratice.html',assess=random_test_type, data=random_question, cat=test_cat, domain=domain, difficulty=difficulty, skill=skill, desmos_api_key=desmos_api_key)

@app.route('/api/random-question')
def api_random_question():
    all_files = os.listdir('./question_data')

    random_test_type = random.choice([f for f in all_files])


    random_category = random.choice([f for f in os.listdir(f'./question_data/{random_test_type}')])
    random_difficulty = random.choice(['Easy', 'Medium', 'Hard'])

    file_name = random_test_type + "_"+ random_category + "_" + random_difficulty + ".json"


    full_path = f'./question_data/{random_test_type}/{random_category}/{file_name}'

    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        random_question = random.choice(data)
        
        # Try standard format first
        if "answerOptions" in random_question and "stem" in random_question:
            pass  # Already in standard format

        # Try alternative 'fore' format
        elif "answer" in random_question and "prompt" in random_question:
            # Convert fore format to standard format
            if "choices" in random_question["answer"]:
                choices = random_question["answer"]["choices"]
                answerOptions = []
                for key in sorted(choices.keys()):
                    answerOptions.append({
                        "content": choices[key]["body"],
                        "id": key
                    })
            else:
                answerOptions = []
            
            correct = random_question["answer"].get("correct_choice", "")
            if isinstance(correct, str):
                correct = [correct.upper()]
            elif isinstance(correct, list):
                correct = [c.upper() for c in correct]
            else:
                correct = []

            random_question = {
                "stimulus": "",
                "stem": random_question.get("prompt", ""),
                "answerOptions": answerOptions,
                "correct_answer": correct,
                "rationale": random_question["answer"].get("rationale", ""),
                "difficulty": random_question.get("difficulty", random_difficulty),
                "skill_desc": random_question.get("skill_desc", random_question.get("skill", "")),
                "primary_class_cd_desc": random_question.get("primary_class_cd_desc", ""),
            }

        # If neither format, use what we have
        else:
            # Ensure we have the required fields for the template
            if "stem" not in random_question:
                random_question["stem"] = random_question.get("prompt", "Question format not recognized.")
            if "answerOptions" not in random_question:
                random_question["answerOptions"] = []
            if "correct_answer" not in random_question:
                random_question["correct_answer"] = []
            if "rationale" not in random_question:
                random_question["rationale"] = ""
        
    # Add the same metadata processing as random_practice route
    if random_category in ['EOI', 'INI', 'SEC', 'CAS']:
        test_cat = ["English"]
    else:
        test_cat = ["Math"]

    try:
        difficulty = random_question['difficulty']
    except:
        difficulty = random_difficulty + "?"
        
    sat_category_map = {
        "P": "Advanced-Math",
        "INI": "Information-and-Ideas",
        "SEC": "Standard-English-Conventions",
        "CAS": "Craft-and-Structure",
        "Q": "Problem-Solving-and-Data-Analysis",
        "EOI": "Expression-of-Ideas",
        "S": "Geometry-and-Trigonometry",
        "H": "Algebra"
    }
    domain = sat_category_map.get(random_category, random_category)
    skill = random_question.get('skill_desc', random_question.get('skill', 'Unknown'))

    # Add metadata to the response
    response_data = random_question.copy()
    response_data['cat'] = test_cat
    response_data['domain'] = domain
    response_data['skill'] = skill
    response_data['difficulty'] = difficulty
    response_data['assess'] = random_test_type
    return jsonify(response_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
 


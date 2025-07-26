import requests
import random
from flask import Flask, render_template
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()
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
# data = load_data()
# print(len(data))

# payload = {"external_id": data[0]['external_id']}
# print(payload)
# response = requests.post(
#     'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
#     json=payload
# )
# #print(response.json())
# print(os.getenv('DESMOS_API_KEY'))


data = load_data(random.randint(1, 8))

random_question_index = random.randint(0, len(data) - 1)
payload = {"external_id": data[random_question_index]['external_id']}
test_cat = data[random_question_index]['general_area'].split('/')
domain = data[random_question_index]['problem_area']
difficulty = data[random_question_index]['difficulty']
response = requests.post(
    'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
    json=payload)
question = response.json()
print(question)
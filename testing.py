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


# data = load_data(random.randint(1, 8))

# random_question_index = random.randint(0, len(data) - 1)
# payload = {"external_id": data[random_question_index]['external_id']}
# test_cat = data[random_question_index]['general_area'].split('/')
# domain = data[random_question_index]['problem_area']
# difficulty = data[random_question_index]['difficulty']
# response = requests.post(
#     'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
#     json=payload)
# question = response.json()
# print(question)
# catagory = [
#     "Cross-Text Connections", ###
#     "Text Structure and Purpose", ###
#     "Words in Context",
#     "Rhetorical Synthesis", ###
#     "Transitions",
#     "Central Ideas and Details",
#     "Command of Evidence",
#     "Inferences",
#     "Boundaries",
#     "Form, Structure, and Sense",
#     "Linear equations in one variable",
#     "Linear functions",
#     "Linear equations in two variables",
#     "Systems of two linear equations in two variables",
#     "Linear inequalities in one or two variables",
#     "Equivalent expressions",
#     "Nonlinear equations in one variable and systems of equations in two variables",
#     "Nonlinear functions",
#     "Ratios, rates, proportional relationships, and units",
#     "Percentages",
#     "One-variable data: Distributions and measures of center and spread",
#     "Two-variable data: Models and scatterplots",
#     "Probability and conditional probability",
#     "Inference from sample statistics and margin of error",
#     "Evaluating statistical claims: Observational studies and experiments",
#     "Area and volume",
#     "Lines, angles, and triangles",
#     "Right triangles and trigonometry",
#     "Circles"
# ]

# encoded = 4
# print(len(catagory)) # 28
# binary_digits = '0'*(29-len(bin(int(encoded))[2:])) + bin(int(encoded))[2:] # → '00000000000000000000000000000100'
# print(binary_digits)
# for index, i in enumerate(binary_digits):
#     if i == '1':
#         print(catagory[index])

catagory = [
    # Algebra
    "Linear equations in one variable",
    "Linear functions",
    "Linear equations in two variables",
    "Systems of two linear equations in two variables",
    "Linear inequalities in one or two variables",
    # Advanced Math
    "Equivalent expressions",
    "Nonlinear equations in one variable and systems of equations in two variables",
    "Nonlinear functions",
    # Problem Solving and Data Analysis
    "Ratios, rates, proportional relationships, and units",
    "Percentages",
    "One-variable data: Distributions and measures of center and spread",
    "Two-variable data: Models and scatterplots",
    "Probability and conditional probability",
    "Inference from sample statistics and margin of error",
    "Evaluating statistical claims: Observational studies and experiments",
    # Geometry and Trigonometry
    "Area and volume",
    "Lines, angles, and triangles",
    "Right triangles and trigonometry",
    "Circles",
    # Craft and Structure
    "Cross-Text Connections",
    "Text Structure and Purpose",
    "Words in Context",
    # Expression of Ideas
    "Rhetorical Synthesis",
    "Transitions",
    # Information and Ideas
    "Central Ideas and Details",
    "Command of Evidence",
    "Inferences",
    # Standard English Conventions
    "Boundaries",
    "Form, Structure, and Sense"
]


catagory.reverse()
print(catagory)
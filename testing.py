import requests

from flask import Flask, render_template
import json
import os
import requests
DATA_FILE = os.path.join(os.path.dirname(__file__), 'questions/Algebra.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}
data = load_data()
print(len(data))

payload = {"external_id": data[0]['external_id']}
print(payload)
response = requests.post(
    'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
    json=payload
)
print(response.json())
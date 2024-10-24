from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.getenv('API_KEY')
genai.configure(api_key=key)

app = Flask(__name__)

# Enable CORS and allow all methods from localhost:3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["POST", "OPTIONS"]}})

def get_specific_analysis(data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        "Analyze this person's sleep and dream quality and try to provide insight into what it could mean and how they can improve their sleep."
        "You are talking directly to the user. This is information on a singular dream for a person. "
        "Please give insight. Make it less than 250 words, with no intro text like \"The person's sleep and dream quality show a ...\", "
        "just start with the feedback. \n" + data
    )
    return response.text

def get_story(data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Make a creative story from the following data. The data is on a person's dream. Make it creative and no more than 300 words.\n" + data)
    return response.text

@app.route('/dreaminsights', methods=['POST', 'OPTIONS'])
def handle_dreaminsight():
    if request.method == 'OPTIONS':
        # Handle the preflight request here
        response = jsonify({'status': 'preflight ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200  # Must return 200 OK for preflight

    elif request.method == 'POST':
        js = request.get_json()
        res = get_specific_analysis(str(js['dream']))
        response = jsonify({'analysis': res})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response, 200
    
@app.route('/story', methods=['POST', 'OPTIONS'])
def handle_story():
    if request.method == 'OPTIONS':
        # Handle the preflight request here
        response = jsonify({'status': 'preflight ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200  # Must return 200 OK for preflight
    elif request.method == 'POST':
        js = request.get_json()
        print(js)
        res = get_story(str(js['dream']))
        print(res)
        response = jsonify({'story': res})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response, 200

if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port)

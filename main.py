import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import requests
import pandas as pd
# import flask
load_dotenv()

key = os.getenv('API_KEY')

genai.configure(api_key=key)

def get_story():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about the following dream: I was walking through a dense forest at night, with a glowing full moon overhead. The trees seemed to stretch endlessly in all directions. As I walked, I heard whispers but couldn’t see anyone. Suddenly, I found an old cabin in a clearing, and the door creaked open by itself. Inside, the furniture was covered in dust, but there was a small, glowing object on the table. When I reached out to touch it, I woke up.")
    print(response.text)

response1 = requests.get('http://localhost:5000/api/dreams/get?userId=67156c65e9acb19c984388ea&dateString=10-20-2024')
response2 = requests.get('http://localhost:5000/api/dreams/get?userId=67156c65e9acb19c984388ea&dateString=10-18-2024')
as_json = json.loads(response1.content)['dream']
as_json2 = json.loads(response2.content)['dream']

df = pd.read_json(json.dumps([as_json, as_json2]), lines=False)

def get_overall_analysis():
    info = ""
    for col in df.columns[3:-3]:
        
        info += f"{col}: {str(df[col].value_counts().to_dict())}" + "\n"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Analyze this person's sleep and dream quality and try to provide insight into what it could mean. You are talking directly to the user. The data is provided in the following format. Each line's first word is the category of information provided, and the subsequent dictionary contains each of the provided responses and their respective frequency. These are dreams on different days for the same person. Please give insight. Make it less than 1000 words, with no intro text like \"The person's sleep and dream quality show a ...\", just start with the feedback. \n" + info)
    print(response.text)

def get_specific_analysis():
    data = str(as_json)
    print(data)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Analyze this person's sleep and dream quality and try to provide insight into what it could mean. You are talking directly to the user. This is information on a singular dream for a person.. Please give insight. Make it less than 1000 words, with no intro text like \"The person's sleep and dream quality show a ...\", just start with the feedback. \n" + data)
    print(response.text)

def get_story():
    data = str(as_json)
    print(data)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Make a creative story from the following data. The data is on a person's dream. Make it creative and no more than 300 words.\n" + data)
    print(response.text)

get_story()


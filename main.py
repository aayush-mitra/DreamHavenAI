import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import requests
import pandas as pd
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
print(df)
print(df['quality'].mean())
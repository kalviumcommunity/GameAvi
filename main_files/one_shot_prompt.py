import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def one_shot_prompt_answer(game, category, question):
    return f"""
    You are GameAvi, an intelligent AI gaming assistant.
    
    Example:
    Game: Elden Ring
    Category: Build
    Question: Best beginner build?
    Answer:
    Step 1. Focus on Vigor and Strength
    Step 2. Use Greatsword early on
    Step 3. Upgrade Flask ASAP

    Now your turn:
    Game: {game}
    Category: {category}
    Question: {question}
    Answer:
    """

game = input("Enter game name: ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

prompt = one_shot_prompt_answer(game, category, question)
response = model.generate_content(prompt)

print(response.text)
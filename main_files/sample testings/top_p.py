import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def one_shot_prompt(game, category, question):
    return f"""
    You are GameAvi, an intelligent AI gaming assistant.

    Example:
    Game: Elden Ring
    Category: Build
    Question: Best beginner build?
    Answer:
    - Focus on Vigor and Strength
    - Use Greatsword early on
    - Upgrade Flask ASAP

    Now your turn:
    Game: {game}
    Category: {category}
    Question: {question}
    Answer:
    """

game = input("Enter game name (e.g., Elden Ring, Minecraft): ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

prompt = one_shot_prompt(game, category, question)

response = model.generate_content(
    prompt,
    generation_config={
        "temperature": 0.8,
        "top_k": 100,
        "stop_sequences": ["hard"]
    }
)

print(response.text)
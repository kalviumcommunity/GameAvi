import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def multi_shot_prompt(game, category, question):
    return f"""
    You are GameAvi, an intelligent AI gaming assistant.

    Example 1:
    Game: Elden Ring
    Category: Build
    Question: Best beginner build?
    Answer:
    - Focus on Vigor and Strength
    - Use Greatsword early on
    - Upgrade Flask ASAP

    Example 2:
    Game: Minecraft
    Category: Survival
    Question: How to survive the first night?
    Answer:
    - Gather wood and craft tools
    - Build a shelter before night
    - Make a bed and sleep to skip night

    Example 3:
    Game: Valorant
    Category: Strategy
    Question: Best agent for beginners?
    Answer:
    - Start with Sage for healing
    - Use abilities to support teammates
    - Focus on map control and positioning

    Now your turn:
    Game: {game}
    Category: {category}
    Question: {question}
    Answer:
    """

game = input("Enter game name (e.g., Elden Ring, Minecraft): ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

prompt = multi_shot_prompt(game, category, question)
response = model.generate_content(prompt, generation_config={"temperature": 1.0}) 

print(response.text)

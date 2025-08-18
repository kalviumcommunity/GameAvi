import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def dynamic_prompt(game, category, question, level, inventory, mode):
    return f"""
    You are GameAvi, an intelligent AI gaming assistant.

    Player Info:
    Game: {game}
    Category: {category}
    Level: {level}
    Inventory: {', '.join(inventory)}
    Mode: {mode}

    Question: {question}

    Give practical step by step, 
    personalized advice based on the player's level, inventory, and mode.
    """

game = input("Enter game name: ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")
level = input("Enter your player level: ")
mode = input("Enter game mode (Normal / Hard / Hard): ")
inventory = input("Enter inventory items (comma-separated): ").split(',')

prompt = dynamic_prompt(game, category, question, level, inventory, mode)
response=model.generate_content(prompt)

print(response.text)
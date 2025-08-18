import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def get_game_advice(game, category, question):
    prompt= f"""
    You are GameAvi an AI gaming assistant.
    Game: {game}
    Category: {category}
    Question: {question}
    
    Provide a clear and practical answer for the player and the answer should be precise 
    and to the point.
    """
    response = model.generate_content(prompt)
    return response.text

game = input("Enter game name (e.g., Elden Ring, Minecraft): ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

answer = get_game_advice(game, category, question)
print("\n--- GameAvi's Advice ---")
print(answer)
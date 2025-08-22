import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def one_shot_prompt(game, category, question):
  return f"""
    You are GameAvi, an intelligent AI gaming assistant.

    Example (structured JSON output):
    {{
        "game": "Elden Ring",
        "category": "Build",
        "question": "Best beginner build?",
        "answer": [
            "Focus on Vigor and Strength",
            "Use Greatsword early on",
            "Upgrade Flask ASAP"
        ]
    }}

    Now your turn:
    game: {game}
    category: {category}
    question: {question}
    Provide the response in the SAME JSON format.
    """

game = input("Enter game name (e.g., Elden Ring, Minecraft): ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

prompt = one_shot_prompt(game, category, question)

response = model.generate_content(prompt, generation_config={
    "temperature": "1.0",
    "top_p": "0.9",
    "top_k": "100",
    "stop_sequences": ["###"]
})

print(response.text)    
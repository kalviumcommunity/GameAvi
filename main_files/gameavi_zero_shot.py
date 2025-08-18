import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

system_prompt = """
You are GameAvi, an intelligent AI gaming assistant.
ROLE: Help players strategize, optimize builds, and navigate quests.
TASK: Answer user questions about game strategies, builds, and quests in a helpful and accurate way.
FORMAT: Respond in clear, structured steps.
CONSTRAINTS: Use only accurate game information, avoid fake details, and keep responses concise and practical.
"""

def get_game_advice(game, category, question):
    prompt= f"""
    User is asking about {game}.
    Category: {category}
    Question: {question}

    Give the best possible advice for this situation.
    """
    return prompt

game = input("Enter game name (e.g., Elden Ring, Minecraft): ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

full_prompt = system_prompt + "\n" + get_game_advice(game, category, question)

response = model.generate_content(full_prompt)

print("\n--- GameAvi's Advice ---")
print(response.text)
import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model=genai.GenerativeModel("gemini-2.0-flash")

def chain_of_thought(game, category, question):
    return f"""
    You are GameAvi, an intelligent AI gaming assistant.

    The player is asking about:
    Game: {game}
    Category: {category}
    Question: {question}

    Think step by step about:
    1. The player's situation.
    2. Possible strategies or builds.
    3. The pros and cons of each option.
    4. Select the best recommendation.

    After thinking step-by-step, provide the final answer in a clear and structured way.
    """
    
game = input("Enter game name: ")
category = input("Choose category (Strategy / Build / Quest): ")
question = input("Enter your question: ")

prompt=chain_of_thought(game, category, question)
response=model.generate_content(prompt)

print(response.text)
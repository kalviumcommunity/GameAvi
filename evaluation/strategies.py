import os, json, time, re
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-1.5-flash"

def call_llm(prompt: str, model_name: str = MODEL_NAME) -> str:
    model = genai.GenerativeModel(model_name)
    for i in range(2):  # simple retry
        try:
            resp = model.generate_content(prompt)
            return (resp.text or "").strip()
        except Exception as e:
            if i == 2: raise
            time.sleep(1 + i)
    return ""

def zero_shot(game: str, category: str, question: str, **_):
    prompt = f"Game: {game}\nCategory: {category}\nQuestion: {question}\nGive practical, concise advice."
    return call_llm(prompt)

def one_shot(game: str, category: str, question: str, **_):
    prompt = f"""
You are GameAvi.
Example:
Game: Elden Ring
Category: Build
Question: Best beginner build?
Answer:
- Focus on Vigor & Strength
- Use simple heavy weapon
- Upgrade Flask

Now answer:
Game: {game}
Category: {category}
Question: {question}
Answer:
"""
    return call_llm(prompt)

def multi_shot(game: str, category: str, question: str, **_):
    prompt = f"""
You are GameAvi.

Example 1:
Game: Elden Ring
Category: Build
Question: Best beginner build?
Answer:
- Vigor/Strength focus
- Greatsword early
- Upgrade Flask

Example 2:
Game: Minecraft
Category: Survival
Question: How to survive the first night?
Answer:
- Gather wood & tools
- Build shelter
- Make a bed or light

Now answer:
Game: {game}
Category: {category}
Question: {question}
Answer:
"""
    return call_llm(prompt)

def dynamic(game: str, category: str, question: str, level: int = None, mode: str = None, inventory: List[str] = None, **_):
    inv = ", ".join(inventory or [])
    prompt = f"""
You are GameAvi.

Player:
- Game: {game}
- Category: {category}
- Level: {level}
- Mode: {mode}
- Inventory: {inv}

Question: {question}

Give step-by-step, personalized advice that uses level, mode, and inventory.
"""
    return call_llm(prompt)

def chain_of_thought(game: str, category: str, question: str, **_):
    prompt = f"""
You are GameAvi.

Think step by step about:
1) Player situation
2) Options
3) Pros/cons
4) Best recommendation

Game: {game}
Category: {category}
Question: {question}

After thinking, give a short final answer in bullet points.
"""
    return call_llm(prompt)

ALL_STRATEGIES = {
    "zero_shot": zero_shot,
    "one_shot": one_shot,
    "multi_shot": multi_shot,
    "dynamic": dynamic,
    "chain_of_thought": chain_of_thought,
}

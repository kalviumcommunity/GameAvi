# evaluation/judge_prompt.py
import os, json, re, time
from typing import Dict
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-1.5-flash"

SYSTEM_INSTRUCTIONS = """
You are an impartial evaluator of AI-generated gaming advice.
Compare the AI's answer against the expected reference.

Criteria (0-5 each):
- Relevance: addresses the user's question and game context.
- Accuracy: factually correct for the game; no fabricated mechanics.
- Completeness: covers the key points in the expected answer.
- Clarity: easy to follow, actionable.

Important:
- Do NOT reveal chain-of-thought. Return only a JSON object.
- If the AI goes beyond the expected but remains correct and useful, you may reward Completeness.
- Penalize hallucinations or unsafe advice.

Your JSON schema:
{
  "relevance": 0-5,
  "accuracy": 0-5,
  "completeness": 0-5,
  "clarity": 0-5,
  "total_score": 0-20,
  "feedback": "one short paragraph with concrete suggestions"
}
"""

def _extract_json(text: str) -> Dict:
    # Grab the first {...} block
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}

def judge(expected: str, actual: str, game: str, category: str, question: str) -> Dict:
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_INSTRUCTIONS)
    prompt = f"""
Game: {game}
Category: {category}
Question: {question}

Expected answer (reference):
{expected}

AI answer:
{actual}

Return ONLY the JSON object as specified.
"""
    for i in range(2):
        try:
            resp = model.generate_content(prompt)
            data = _extract_json(resp.text or "")
            if data and "total_score" in data: return data
        except Exception:
            if i == 2: raise
            time.sleep(1 + i)
    return {"relevance":0,"accuracy":0,"completeness":0,"clarity":0,"total_score":0,"feedback":"Failed to parse judge output."}

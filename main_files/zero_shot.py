import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

prompt = "Explain the best strategy for a beginner in God Of War."

response = model.generate_content(prompt)

print("Prompt:", prompt)
print("Response:\n", response.text)

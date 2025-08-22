import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

embedding_model = "models/embedding-001"

def generate_embeddings(text):
    response = genai.embed_content(
        model=embedding_model,
        content=text
    )
    return response['embedding']

text = input("Enter text to generate embeddings: ")
embedding_vector = generate_embeddings(text)

print(f"Text: {text}")
print(f"Embedding length: {len(embedding_vector)}")
print(f"Embedding (first 10 values): {embedding_vector[:10]}")

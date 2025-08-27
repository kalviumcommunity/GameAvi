import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
EMBEDDING_MODEL = "models/embedding-001"

def generate_embedding(text):
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return response['embedding']


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == "__main__":
    text1 = input("Enter first text: ")
    text2 = input("Enter second text: ")
    
    print("\nGenerating embeddings...")
    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)
    
    print(f"Embedding 1 length: {len(embedding1)}")
    print(f"Embedding 2 length: {len(embedding2)}")
    
    similarity = cosine_similarity(embedding1, embedding2)
    print(f"\nCosine Similarity between the two texts: {similarity:.4f}")
    
    if similarity > 0.8:
        print("The texts are highly similar.")
    elif similarity > 0.5:
        print("The texts are somewhat similar.")
    else:
        print("The texts are different.")

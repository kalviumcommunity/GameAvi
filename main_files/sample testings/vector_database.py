# embedding_model = "models/embedding-001"


# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index_name = "gemini-embeddings"

# if index_name not in [i.name for i in pc.list_indexes()]:
#     pc.create_index(
#         name=index_name,
#         dimension=768,
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENV"))  # Example: us-east-1
#     )

# index = pc.Index(index_name)

# def generate_embeddings(text):
#     response = genai.embed_content(model=embedding_model, content=text)
#     return response['embedding']

# def store_embedding(id, text):
#     embedding_vector = generate_embeddings(text)
#     index.upsert([(id, embedding_vector, {"text": text})])
#     return embedding_vector

# def search_similar(query, top_k=3):
#     query_embedding = generate_embeddings(query)
#     result = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#     return result

# text = input("Enter text to store in vector DB: ")
# embedding_vector = store_embedding("doc1", text)

# print(f"Stored embedding for: {text}")
# print(f"Embedding length: {len(embedding_vector)}")

# query = input("Enter search query: ")
# results = search_similar(query)
# print("Top matches:")
# for match in results['matches']:
#     print(f"- {match['metadata']['text']} (Score: {match['score']})")

import os
import google.generativeai as genai
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "gemini-embeddings"
pinecone_region = os.getenv("PINECONE_ENV", "us-east-1")  # Default region

# Generate embeddings using Gemini
def generate_embeddings(text):
    model = "models/embedding-001"
    embedding_response = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document"
    )
    return embedding_response["embedding"]

# Auto-detect dimension
print("🔍 Generating sample embedding to detect dimension...")
sample_embedding = generate_embeddings("test")
dimension = len(sample_embedding)
print(f"✅ Embedding dimension detected: {dimension}")

# Check existing indexes
existing_indexes = [i.name for i in pc.list_indexes()]
if index_name in existing_indexes:
    # Check if dimension matches
    index_info = pc.describe_index(index_name)
    if index_info.dimension != dimension:
        print(f"⚠ Dimension mismatch! Existing: {index_info.dimension}, Required: {dimension}")
        print("🗑 Deleting old index and creating a new one...")
        pc.delete_index(index_name)
    else:
        print("✅ Existing index has correct dimension. Skipping creation.")

# Create index if it doesn't exist
if index_name in existing_indexes:
    index_info = pc.describe_index(index_name)
    if index_info.dimension != dimension:
        print(f"⚠ Dimension mismatch! Existing: {index_info.dimension}, Required: {dimension}")
        print("🗑 Deleting old index and creating a new one...")
        pc.delete_index(index_name)
        # Wait until index is deleted
        while index_name in [i.name for i in pc.list_indexes()]:
            print("⏳ Waiting for index to be deleted...")
else:
    print("✅ No existing index found.")

# Create the index
print(f"📦 Creating new index: {index_name} with dimension {dimension}")
pc.create_index(
    name=index_name,
    dimension=dimension,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region=pinecone_region)
)

# Connect to the index
index = pc.Index(index_name)
print("✅ Connected to Pinecone index.")

# Store a sample embedding
text_to_embed = "Hello, this is a test for Pinecone integration with Gemini embeddings."
embedding = generate_embeddings(text_to_embed)

print("⬆ Uploading vector to Pinecone...")
index.upsert(vectors=[
    {
        "id": "test-id",
        "values": embedding,
        "metadata": {"text": text_to_embed}
    }
])
print("✅ Vector uploaded successfully!")

# Perform a query
print("🔍 Performing similarity search...")
query_embedding = generate_embeddings("Hi, this is a test query.")
results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
print("✅ Query results:")
for match in results["matches"]:
    print(f"- ID: {match['id']}, Score: {match['score']}, Text: {match['metadata']['text']}")

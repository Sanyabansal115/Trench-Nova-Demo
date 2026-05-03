from pinecone import Pinecone, ServerlessSpec

# 1. Initialize the client with your API Key
pc = Pinecone(api_key="pcsk_4FTbdW_MyKfPKX2DrSKwTtVrixyNY86kFdwbCMh5jDtBpmAnt53zT8hGjvYLsoVP8HoVDT")

# 2. Create or connect to an index
# 'dimension' must match the output of your embedding model (e.g., 384 for MiniLM)
index_name = "quickstart"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384, 
        metric="cosine", # Measures the angle between vectors (standard for text)
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# 3. Upsert (Upload) your data
# This is how you "train" the vault with your documents
# Generate a test embedding vector (384 dimensions to match MiniLM)
test_embedding = [0.1] * 384  # Create a vector of 384 values

vectors_to_upload = [
    {
        "id": "doc_1", 
        "values": test_embedding,
        "metadata": {"text": "The tax firm offers cloud accounting."}
    }
]

index.upsert(vectors=vectors_to_upload)
print("Data stored successfully!")
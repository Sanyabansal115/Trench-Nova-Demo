from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os

# Load environment variables from .env file manually
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('\'"')

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("YOUR_PINECONE_API_KEY"))
index = pc.Index("quickstart")

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create the search vector
query_embedding = model.encode("How can a tax firm move to the cloud?")

# Query Pinecone
results = index.query(
    vector=query_embedding.tolist(),
    top_k=3,  # Get the top 3 most similar chunks
    include_metadata=True
)

# Print the found matches
print("Search Results:")
for match in results['matches']:
    print(f"Match Found: {match['metadata']['text']}")
    print(f"Score: {match['score']}\n")

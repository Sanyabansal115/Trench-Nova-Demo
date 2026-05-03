from sentence_transformers import SentenceTransformer

# 1. Load a pre-trained model
# 'all-MiniLM-L6-v2' is popular, fast, and very effective for search.
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define your text
sentences = ["The tax firm offers specialized cloud accounting.", 
             "Cloud-based solutions for financial management."]

# 3. Generate the embeddings (The Vectorization)
embeddings = model.encode(sentences)

# 4. Look at the result
print(f"Vector dimension: {len(embeddings[0])}")
print(f"First 5 numbers of the vector: {embeddings[0][:5]}")
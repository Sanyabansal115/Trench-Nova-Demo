from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os

app = Flask(__name__)

# Comprehensive CORS setup
cors_config = {
    "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}
CORS(app, resources={r"/*": cors_config})

# Add request logging
@app.before_request
def log_request():
    if request.method != 'OPTIONS':  # Skip logging OPTIONS preflight requests
        print(f"\n📨 Incoming request: {request.method} {request.path}")
        if request.is_json:
            print(f"   Data: {request.get_json()}")
        print("---")

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
try:
    pc = Pinecone(api_key=os.getenv("YOUR_PINECONE_API_KEY"))
    index = pc.Index("quickstart")
    print("✓ Pinecone client initialized successfully")
except Exception as e:
    print(f"✗ Error initializing Pinecone: {e}")
    raise

# Load the embedding model
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ SentenceTransformer model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    raise

@app.route('/search', methods=['POST', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        # Explicitly allow the headers the browser is asking for
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    # For the actual POST request:
    try:
        data = request.get_json(force=True)  # Use force=True to be safer
        query = data.get('query')
        top_k = data.get('top_k', 5)
        
        print(f"📝 Search query received: '{query}'")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Create the search vector
        query_embedding = model.encode(query)
        print(f"✓ Query encoded to vector (dimension: {len(query_embedding)})")
        
        # Query Pinecone
        results = index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results for frontend
        formatted_results = []
        for match in results['matches']:
            formatted_results.append({
                'id': match['id'],
                'score': match['score'],
                'text': match['metadata'].get('text', ''),
            })
        
        print(f"✓ Found {len(formatted_results)} results")
        return jsonify({"results": formatted_results})
    
    except Exception as e:
        print(f"✗ Error during search: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is alive"}), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting Trench Nova API Server")
    print("="*50)
    print("Flask API running on http://localhost:5000")
    print("Search endpoint: POST http://localhost:5000/search")
    print("Health check: GET http://localhost:5000/health")
    print("="*50 + "\n")
    app.run(port=5000, debug=False, use_reloader=False)

# 🚀 Trench Nova: Semantic Search Demo

A full-stack semantic search application that combines **React frontend**, **Python Flask backend**, **Pinecone vector database**, and **SentenceTransformer embeddings** to deliver intelligent document search with confidence scoring.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Technologies Used](#technologies-used)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Trench Nova** is a semantic search engine designed to help users find relevant information based on meaning rather than keyword matching. It uses:

- **Vector embeddings** to convert text into numerical representations
- **Pinecone** to store and retrieve similar vectors
- **SentenceTransformer** for fast, accurate embeddings
- **React** for an interactive search interface
- **Flask** as the backend API

Perfect for portfolio demonstrations, tax firms migrating to cloud solutions, or any knowledge base search use case.

---

## ✨ Features

✅ **Semantic Search** - Find results based on meaning, not keywords  
✅ **Confidence Scores** - View match reliability as percentages  
✅ **Real-time Latency** - Monitor client-side response times  
✅ **CORS Enabled** - Frontend and backend run independently  
✅ **Error Handling** - Detailed error messages for debugging  
✅ **Scalable Architecture** - Separate frontend (port 3000) and backend (port 5000)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (3000)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Search Component (Search.jsx)                       │  │
│  │  - Query input                                       │  │
│  │  - Results display                                   │  │
│  │  - Confidence score calculation                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬─────────────────────────────────────────────┘
                 │ axios.post("http://localhost:5000/search")
                 │
┌────────────────▼─────────────────────────────────────────────┐
│                   Flask API (5000)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /search Endpoint                                    │  │
│  │  - Receives query                                    │  │
│  │  - Encodes with SentenceTransformer                  │  │
│  │  - Queries Pinecone index                            │  │
│  │  - Returns formatted results                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬─────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────┐
│            Pinecone Vector Database (Cloud)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Index: "quickstart"                                 │  │
│  │  Dimension: 384 (all-MiniLM-L6-v2)                   │  │
│  │  Metric: Cosine Similarity                           │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

- **Python 3.9+** (with conda or venv)
- **Node.js 14+** and npm
- **Pinecone API Key** (free tier available)
- **Git** (optional, for version control)

---

## 📁 Project Structure

```
Trench Nova demo/
├── .env                          # API keys and secrets
├── README.md                      # This file
├── api.py                         # Flask backend server
├── embed.py                       # Embedding generation utility
├── populate_pinecone.py          # Script to upload data to Pinecone
├── search.py                      # Standalone search utility
├── frontend/
│   ├── package.json              # Node.js dependencies
│   ├── webpack.config.js         # Webpack build configuration
│   ├── public/
│   │   └── index.html            # HTML template
│   └── src/
│       ├── index.jsx             # React entry point
│       ├── App.jsx               # Main App component
│       └── components/
│           └── Search.jsx        # Search component
└── node_modules/                 # Frontend dependencies
```

---

## 🔧 Installation

### Step 1: Clone/Setup the Project

```bash
cd "C:\Users\sanya\OneDrive\Desktop\Trench Nova demo"
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install Python dependencies
pip install flask flask-cors sentence-transformers pinecone-client
```

### Step 3: Configure Environment Variables

Create `.env` file in the root directory:

```env
YOUR_PINECONE_API_KEY='your_actual_api_key_here'
```

**Get your API key:**
1. Go to [pinecone.io](https://www.pinecone.io)
2. Sign up for free tier
3. Create an index named `quickstart`
4. Copy your API key

### Step 4: Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# This installs:
# - react, react-dom
# - axios (for HTTP requests)
# - webpack, webpack-cli, webpack-dev-server
# - babel-loader (for JSX)
# - html-webpack-plugin
```

---

## 🚀 Running the Application

### Terminal 1: Start Flask Backend

```bash
cd "C:\Users\sanya\OneDrive\Desktop\Trench Nova demo"
python api.py
```

You should see:
```
✓ Pinecone client initialized successfully
✓ SentenceTransformer model loaded successfully

==================================================
🚀 Starting Trench Nova API Server
==================================================
Flask API running on http://localhost:5000
Search endpoint: POST http://localhost:5000/search
Health check: GET http://localhost:5000/health
==================================================
```

### Terminal 2: Start React Frontend

```bash
cd frontend
npm start
```

You should see:
```
[webpack-dev-server] Project is running at:
[webpack-dev-server] Loopback: http://localhost:3000/
```

Browser will automatically open to `http://localhost:3000`

---

## 📡 API Documentation

### POST /search

**Request:**
```json
{
  "query": "How can a tax firm move to the cloud?",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "doc_1",
      "score": 0.0456,
      "text": "Cloud-based solutions for financial management..."
    },
    {
      "id": "doc_2",
      "score": 0.0389,
      "text": "Tax firms benefit from cloud infrastructure..."
    }
  ]
}
```

**Parameters:**
- `query` (string, required): Search query
- `top_k` (integer, optional): Number of results to return (default: 5)

**Response Fields:**
- `id`: Document identifier in Pinecone
- `score`: Distance metric (lower = more similar)
- `text`: Document text/metadata

### GET /health

**Response:**
```json
{
  "status": "API is alive"
}
```

---

## 🔄 Data Population

### Step 1: Generate Embeddings

Run `embed.py` to test embedding generation:

```bash
python embed.py
```

This will output:
```
Vector dimension: 384
First 5 numbers of the vector: [0.123, -0.456, 0.789, ...]
```

### Step 2: Populate Pinecone

Run `populate_pinecone.py` to upload test data:

```bash
python populate_pinecone.py
```

Expected output:
```
Data stored successfully!
```

### Step 3: Search

Run `search.py` to test the search locally:

```bash
python search.py
```

This will return search results without needing the web interface.

---

## 🛠️ Technologies Used

### Frontend
- **React 18.2** - UI framework
- **Axios 1.4** - HTTP client
- **Webpack 5** - Module bundler
- **Babel** - JSX transpiler
- **JSX** - React template syntax

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **SentenceTransformers** - Text embedding model (all-MiniLM-L6-v2)
- **Pinecone** - Vector database
- **Python 3.9+**

### Infrastructure
- **Port 3000** - React dev server
- **Port 5000** - Flask API server
- **Pinecone Cloud** - Vector storage

---

## ⚙️ Configuration

### Search Parameters

Edit `api.py` to adjust:

```python
# Vector dimension (must match embedding model)
dimension=384

# Similarity metric
metric="cosine"  # Options: cosine, euclidean, dotproduct

# Cloud provider
cloud="aws"
region="us-east-1"

# Top-k results (frontend can override)
top_k=5
```

### Frontend Styling

Edit `frontend/src/components/Search.jsx` to customize:
- Input field styles
- Result display format
- Error message appearance
- Confidence score display

### Embedding Model

To use a different embedding model, edit `api.py`:

```python
# Current (384-dim, fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Alternatives:
# model = SentenceTransformer('all-mpnet-base-v2')  # 768-dim, slower, more accurate
# model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
```

**Note:** If you change the model dimension, update `populate_pinecone.py` and recreate your Pinecone index.

---

## 🐛 Troubleshooting

### Issue: "Search failed: Network Error"

**Cause:** Flask API not running

**Solution:**
1. Ensure `python api.py` is running in Terminal 1
2. Check that no other process is using port 5000:
   ```bash
   netstat -ano | findstr :5000  # Windows
   ```
3. If port is in use, kill the process or use a different port

### Issue: "Unsupported Media Type (415)"

**Cause:** CORS preflight not handled correctly

**Solution:**
1. Ensure Flask is at version 2.0+:
   ```bash
   pip install --upgrade flask flask-cors
   ```
2. Restart Flask API
3. Check browser console for detailed error

### Issue: "Invalid API Key"

**Cause:** Pinecone API key not loaded or expired

**Solution:**
1. Verify `.env` file exists with correct key:
   ```bash
   cat .env
   ```
2. Regenerate key in Pinecone dashboard
3. Test with health check:
   ```bash
   curl http://localhost:5000/health
   ```

### Issue: "Resource quickstart not found"

**Cause:** Pinecone index doesn't exist

**Solution:**
1. Create index in Pinecone dashboard, OR
2. Run `python populate_pinecone.py` to auto-create it

### Issue: "SentenceTransformer model not found"

**Cause:** First run downloads ~400MB model

**Solution:**
1. First run will take 2-5 minutes
2. Ensure you have internet connection
3. Model is cached after first download
4. Model location: `~/.cache/huggingface/`

### Issue: "Module not found" errors

**Cause:** Missing Python or npm dependencies

**Solution:**
```bash
# Python
pip install flask flask-cors sentence-transformers pinecone-client

# Node.js
cd frontend && npm install
```

### Issue: Webpack build fails

**Cause:** Missing Babel configuration

**Solution:**
1. Ensure `webpack.config.js` exists
2. Reinstall devDependencies:
   ```bash
   cd frontend && npm install
   ```
3. Try clearing cache:
   ```bash
   npm cache clean --force
   ```

---

## 📊 Performance Tips

1. **First Search Slow?** Model download/cache on first use (normal)
2. **Improve Accuracy** Use larger embedding model (e.g., `all-mpnet-base-v2`)
3. **Scale to Production** Deploy with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```
4. **Optimize Frontend** Build for production:
   ```bash
   cd frontend && npm run build
   ```

---

## 🌐 Deployment Checklist

- [ ] Set up Pinecone production index
- [ ] Generate secure API key
- [ ] Deploy Flask to Render, Railway, or Heroku
- [ ] Deploy React build to Vercel, Netlify, or GitHub Pages
- [ ] Configure CORS for production domains
- [ ] Set up monitoring/logging
- [ ] Add rate limiting to API
- [ ] Enable HTTPS/SSL

---

## 📝 License

Created for portfolio demonstration purposes.

---

## 🙋 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Review Flask terminal logs for errors
3. Open browser DevTools (F12) for frontend errors
4. Verify all prerequisites are installed

---

**Happy Searching! 🔍**

Built with ❤️ for semantic search excellence.

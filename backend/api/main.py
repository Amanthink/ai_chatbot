from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
import os
import pickle

# 🔧 Initialize FastAPI once
app = FastAPI()

# 🔓 Allow CORS (cross-origin requests from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Load the graph safely
try:
    graph_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'graph.gpickle')
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)
    print("✅ Graph loaded successfully.")
except Exception as e:
    print("❌ Failed to load graph:", e)
    G = None

# 📬 Define the data model for /ask endpoint
class Query(BaseModel):
    question: str

# 🔍 POST /ask endpoint
@app.post("/ask")
def ask_question(query: Query):
    q = query.question.lower()
    if G:
        for node in G.nodes():
            if node.lower() in q:
                neighbors = list(G.neighbors(node))
                if neighbors:
                    return {"answer": f"{node} is related to: {', '.join(neighbors)}"}
                return {"answer": f"{node} found, but has no relations."}
    return {"answer": "Sorry, I couldn’t find an answer."}

# 👋 GET /hello endpoint
@app.get("/hello")
def say_hello():
    return {"message": "Hello from your FastAPI bot!"}

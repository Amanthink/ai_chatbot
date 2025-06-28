
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
from pydantic import BaseModel
import os
import pickle

# Corrected graph loading
try:
    graph_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'graph.gpickle')
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)
    print("✅ Graph loaded successfully.")
except Exception as e:
    print("❌ Failed to load graph:", e)
    G = None


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
G = nx.read_gpickle("../data/graph.gpickle")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    q = query.question.lower()
    for node in G.nodes():
        if node.lower() in q:
            neighbors = list(G.neighbors(node))
            if neighbors:
                return {"answer": f"{node} is related to: {', '.join(neighbors)}"}
            return {"answer": f"{node} found, but has no relations."}
    return {"answer": "Sorry, I couldn’t find an answer."}


---

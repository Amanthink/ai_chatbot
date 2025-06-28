
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
from pydantic import BaseModel

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

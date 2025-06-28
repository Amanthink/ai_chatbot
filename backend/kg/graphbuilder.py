import networkx as nx
from backend.nlp.entity_extractor import extract_entities

def build_graph(text):
    G = nx.Graph()
    entities = extract_entities(text)
    for i in range(len(entities) - 1):
        e1, _ = entities[i]
        e2, _ = entities[i + 1]
        G.add_node(e1)
        G.add_node(e2)
        G.add_edge(e1, e2, relation="related_to")
    return G

if __name__ == "__main__":
    with open("../data/raw_text.txt", "r", encoding="utf-8") as f:
        content = f.read()
    G = build_graph(content)
    nx.write_gpickle(G, "../data/graph.gpickle")


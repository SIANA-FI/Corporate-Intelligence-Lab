import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Lecture des données

ownership_df = pd.read_csv(
    "data/ownership.csv"
)

# Création du graphe

G = nx.DiGraph()

for _, row in ownership_df.iterrows():

    parent = row["Parent"]
    subsidiary = row["Subsidiary"]
    ownership = row["Ownership"]

    G.add_edge(
        parent,
        subsidiary,
        weight=ownership
    )

# Affichage

plt.figure(figsize=(12, 8))

pos = nx.spring_layout(
    G,
    seed=42
)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3500,
    font_size=10,
    arrows=True
)

edge_labels = nx.get_edge_attributes(
    G,
    "weight"
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels
)

plt.title(
    "Corporate Ownership Structure"
)

plt.savefig(
    "outputs/ownership_graph.png",
    bbox_inches="tight"
)

plt.close()

print(
    "\nGraph generated : outputs/ownership_graph.png"
)
# gui/pages/frame/algos/kruskal_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Kruskal import kruskal  # Adjust the import according to your project structure
from data.graph_data import graph  # Adjust the import according to your project structure

class KruskalPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.visualiser_kruskal_graphe()

    def visualiser_kruskal_graphe(self):
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        # Get MST edges from Kruskal's algorithm
        mst_edges = kruskal(sommets, matrice_adjacence)
     

        # Create the graph from the adjacency matrix
        G = nx.Graph()
        G.add_nodes_from(sommets)

        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice_adjacence[i][j]
                if poids > 0:
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        # Prepare MST edges for comparison
        mst_set = set()
        for u, v, w in mst_edges:
            # Use frozenset to ignore edge direction and include weight
            mst_set.add((frozenset({u, v}), w))

        # Collect edges in G that are part of the MST
        mst_edges_g = []
        for u, v, data in G.edges(data=True):
            w = data['weight']
            if (frozenset({u, v}), w) in mst_set:
                mst_edges_g.append((u, v))

        # Clear previous canvas
        if self.canvas_widget:
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 5))
        pos = nx.spring_layout(G, seed=42)  # Consistent layout

        # Draw all nodes
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300, node_color="gray")

        # Draw all edges (non-MST)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), edge_color="black", width=1)

        # Highlight MST edges
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=mst_edges_g, edge_color="red", width=3)

        # Draw labels for nodes and edges
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_color='red', font_size=7)

        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
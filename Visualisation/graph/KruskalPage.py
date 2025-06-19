# gui/pages/frame/algos/kruskal_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import ttk

class KruskalPage(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.canvas_widget = None
        
        # Main frame with padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Back button at top right
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        
        
        # Informative title
        title_label = ttk.Label(
            main_frame,
            text=f"Arbre Couvrant Minimal (Algorithme de Kruskal)",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Frame for visualization with border
        viz_frame = ttk.LabelFrame(main_frame, text="Visualisation du graphe et de l'arbre couvrant minimal")
        viz_frame.pack(fill="both", expand=True)
        
        # Internal frame for canvas
        canvas_frame = ttk.Frame(viz_frame)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create visualization immediately
        self.visualiser_kruskal_graphe(canvas_frame)
    
    def return_to_input(self):
        """Retourne à la page d'entrée"""
        if self.controller:
            self.controller.change_frame("InputGraphPage")

    def visualiser_kruskal_graphe(self, parent_frame):
        """Visualise le graphe avec l'arbre couvrant minimal"""
        if not self.data:
            return
            
        sommets = self.data['sommets']
        matrice = self.data['matrice']
        mst_edges = self.data['mst_edges']
        total_weight = self.data['total_weight']

        # Create the graph
        G = nx.Graph()
        G.add_nodes_from(sommets)

        # Add edges from adjacency matrix
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice[i][j]
                if poids > 0:
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        # Prepare MST edges for comparison
        mst_set = set()
        for u, v, w in mst_edges:
            mst_set.add((frozenset({u, v}), w))

        # Collect edges in G that are part of the MST
        mst_edges_g = []
        for u, v, data in G.edges(data=True):
            w = data['weight']
            if (frozenset({u, v}), w) in mst_set:
                mst_edges_g.append((u, v))

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f0f0f0')  # Light background to match theme
        
        # Node positioning
        pos = nx.spring_layout(G, seed=42)  # Consistent layout

        # Draw all nodes
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=800, node_color="lightblue")

        # Draw all edges (non-MST)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), edge_color="gray", width=1.5)

        # Highlight MST edges
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=mst_edges_g, edge_color="red", width=3)

        # Draw labels for nodes and edges
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_color='red', font_size=9)

        # Set title with total weight
        ax.set_title(f"Arbre Couvrant Minimal (Kruskal) - Poids total: {total_weight}", fontsize=12, pad=15)
        
        # Disable axes
        ax.set_axis_off()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Store reference to prevent garbage collection
        self.canvas_widget = canvas


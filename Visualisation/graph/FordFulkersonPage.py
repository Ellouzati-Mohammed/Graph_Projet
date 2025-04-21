import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.FordFulkerson import fordFulkerson
from data.graph_data import graph 

class FordFulkersonPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.visualiser_ford_fulkerson()

    def visualiser_ford_fulkerson(self):
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        # Sélection des nœuds source et puits
        source = sommets[0]
        sink = sommets[-1]

        # Calcul du flot maximum avec Ford-Fulkerson
        try:
            max_flow, residual_graph = fordFulkerson(sommets, matrice_adjacence, source, sink)
        except ValueError as e:
            print(f"Erreur: {e}")
            max_flow = 0
            residual_graph = {}

        # Création du graphe orienté
        G = nx.DiGraph()
        G.add_nodes_from(sommets)
        
        # Ajout des arêtes avec capacités
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                if matrice_adjacence[i][j] > 0:
                    G.add_edge(sommets[i], sommets[j], 
                              capacity=matrice_adjacence[i][j],
                              flow=matrice_adjacence[i][j] - residual_graph[sommets[i]][sommets[j]])

        # Nettoyage du canvas précédent
        if self.canvas_widget:
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)

        # Couleurs et largeurs des arêtes
        edge_colors = []
        edge_widths = []
        for u, v, data in G.edges(data=True):
            if data['flow'] > 0:
                edge_colors.append('red')
                edge_widths.append(2 + data['flow'] * 0.5)
            else:
                edge_colors.append('gray')
                edge_widths.append(1)

        # Dessin du graphe
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=800,
                              node_color='lightblue')
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12,
                               font_weight='bold')
        
        # Dessin des arêtes avec flots
        edges = nx.draw_networkx_edges(
            G, pos, ax=ax, edge_color=edge_colors,
            width=edge_widths, arrows=True,
            arrowstyle='->', arrowsize=20
        )

        # Affichage des capacités et flots
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            edge_labels[(u, v)] = f"{data['flow']}/{data['capacity']}"
        
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels,
            ax=ax, font_color='darkred', font_size=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )

        # Ajout du titre avec le flot maximum
        title = f"Flot maximum: {max_flow}\nSource: {source}, Puits: {sink}"
        ax.set_title(title, fontsize=14, pad=20)

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
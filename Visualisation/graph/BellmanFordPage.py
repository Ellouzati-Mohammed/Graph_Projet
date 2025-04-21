import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.BellmanFord import bellmanFord
from data.graph_data import graph 

class BellmanFordPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.visualiser_bellman_ford_graphe()

    def visualiser_bellman_ford_graphe(self):
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        # Sélection des nœuds de départ et d'arrivée
        debut = sommets[0]
        depart = sommets[-1]

        # Calcul du chemin avec Bellman-Ford
        try:
            chemin = bellmanFord(sommets, matrice_adjacence, debut, depart)
        except ValueError as e:
            print(f"Erreur: {e}")
            chemin = []

        # Création du graphe orienté
        G = nx.DiGraph()
        G.add_nodes_from(sommets)
        
        # Ajout des arêtes pondérées
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice_adjacence[i][j]
                if poids > 0:
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        # Nettoyage du canvas précédent
        if self.canvas_widget:
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent

        # Couleurs des nœuds et arêtes
        node_colors = ['green' if sommet in chemin else 'lightblue' for sommet in sommets]
        path_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)] if len(chemin) > 1 else []
        edge_colors = ['red' if (u, v) in path_edges else 'gray' for u, v in G.edges()]
        edge_widths = [3 if (u, v) in path_edges else 1 for u, v in G.edges()]

        # Dessin du graphe
        nx.draw(
            G, pos, ax=ax, with_labels=True,
            node_color=node_colors, 
            edge_color=edge_colors,
            width=edge_widths,
            node_size=800,
            font_size=12,
            font_weight="bold",
            arrows=True,
            arrowstyle='->',
            arrowsize=15
        )

        # Affichage des poids des arêtes
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=edge_labels,
            ax=ax,
            font_color='darkred',
            font_size=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )

        # Ajout du titre avec le chemin trouvé
        title = f"Chemin le plus court: {' -> '.join(chemin)}" if chemin else "Aucun chemin trouvé"
        ax.set_title(title, fontsize=14)

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
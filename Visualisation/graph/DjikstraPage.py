# gui/pages/frame/algos/dijkstra_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Djikstra import djikstra  # Assurez-vous que le chemin d'import est correct
from tkinter import ttk

class DijkstraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None
        self.controller = None
        self.configure(bg="#f0f0f0")

        # Cadre principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.configure(style="TFrame")

        # Titre
        title_label = ttk.Label(
            main_frame,
            text="Résultat de l'algorithme de Dijkstra",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
            background="#f0f0f0"
        )
        title_label.pack(pady=(0, 10))

        # Cadre pour les contrôles
        self.controls_frame = ttk.Frame(main_frame)
        self.controls_frame.pack(fill="x", pady=(0, 10))
        self.controls_frame.configure(style="TFrame")

        # Cadre pour la visualisation
        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(fill="both", expand=True)
        self.viz_frame.configure(style="TFrame")

        # Variables pour les sélections
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()

    def set_data(self, data):
        """Configure les données et met à jour l'affichage"""
        self.data = data
        self.sommets = data.get('sommets', [])
        self.edges = data.get('edges', [])
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        
        # Afficher le graphe
        self.afficher_graphe_depuis_data()

    def afficher_graphe_depuis_data(self):
        """Affiche le graphe avec le chemin le plus court"""
        if not self.data or not self.sommets or not self.edges:
            return
            
        # Créer la matrice d'adjacence
        n = len(self.sommets)
        sommet_index = {s: i for i, s in enumerate(self.sommets)}
        matrice_adjacence = [[float('inf')] * n for _ in range(n)]
        
        for u, v, w in self.edges:
            i, j = sommet_index[u], sommet_index[v]
            matrice_adjacence[i][j] = w
        
        for i in range(n):
            matrice_adjacence[i][i] = 0

        # Appliquer Dijkstra
        try:
            chemin = djikstra(self.sommets, matrice_adjacence, self.start, self.end)
        except Exception as e:
            print(f"Erreur Dijkstra: {e}")
            chemin = []

        # Créer le graphe
        G = nx.DiGraph()
        G.add_nodes_from(self.sommets)
        
        for u, v, w in self.edges:
            G.add_edge(u, v, weight=w)

        # Nettoyer le canvas précédent s'il existe
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        # Créer une nouvelle figure
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#f0f0f0')  # Fond clair
        
        # Positionnement des nœuds
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent
        
        # Couleurs des nœuds et arêtes
        node_colors = ["#4a6baf" if chemin and sommet in chemin else "#2c3e50" for sommet in self.sommets]
        path_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)] if len(chemin) > 1 else []
        edge_colors = ["#4a6baf" if (u, v) in path_edges else "#adb5bd" for u, v in G.edges()]
        edge_widths = [3 if (u, v) in path_edges else 1 for u, v in G.edges()]

        # Dessin du graphe
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=node_colors, 
            node_size=1500,
            ax=ax,
            alpha=0.9,
            linewidths=0,
        )
        nx.draw_networkx_edges(
            G, pos, 
            edge_color=edge_colors,
            width=edge_widths,
            arrows=True,
            arrowstyle='->',
            arrowsize=20,
            ax=ax,
            alpha=0.7,
        )
        nx.draw_networkx_labels(
            G, pos, 
            font_size=11,
            font_weight="bold",
            font_color="white",
            ax=ax
        )

        # Affichage des poids des arêtes
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=edge_labels,
            ax=ax,
            font_color='#495057',
            font_size=9,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )
        
        # Ajouter le titre avec les informations
        if chemin:
            distance = 0
            for i in range(len(chemin) - 1):
                u, v = chemin[i], chemin[i+1]
                distance += G[u][v]['weight']
            
            title = (
                f"Plus court chemin: {' → '.join(chemin)}\n"
                f"Distance totale: {distance}"
            )
        else:
            title = f"Aucun chemin trouvé entre {self.start} et {self.end}"
        
        ax.set_title(title, fontsize=13, fontweight="bold", pad=16)
        ax.set_axis_off()
        plt.tight_layout()

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        self.canvas_widget = canvas
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
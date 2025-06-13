# gui/pages/frame/algos/dijkstra_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Djikstra import djikstra  # Assurez-vous que le chemin d'import est correct
from data.graph_data import graph  # Adaptez selon votre structure
from tkinter import ttk

class DijkstraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None
        self.controller = None
        
        # Créer un cadre principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bouton de retour
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
      

        # Cadre pour les contrôles
        self.controls_frame = ttk.Frame(main_frame)
        self.controls_frame.pack(fill="x", pady=(0, 10))
        
        # Variables pour les sélections
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        
        # Cadre pour la visualisation
        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(fill="both", expand=True)

    def return_to_input(self):
        """Retourne à la page d'entrée"""
        if self.controller:
            self.controller.change_frame("InputGraphPage")

    def set_data(self, data):
        """Configure les données et met à jour l'affichage"""
        self.data = data
        self.sommets = data.get('sommets', [])
        self.edges = data.get('edges', [])
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        
        # Mettre à jour les contrôles
        self.update_controls()
        
        # Afficher le graphe
        self.afficher_graphe_depuis_data()

    def update_controls(self):
        """Met à jour les menus déroulants de sélection"""
        # Nettoyer les anciens contrôles
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
            
        if not self.sommets:
            return
        
      
    def on_selection_change(self, event=None):
        """Appelé quand la sélection change"""
        self.start = self.source_var.get()
        self.end = self.dest_var.get()
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
            from algorithms.graph.Djikstra import djikstra
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
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f0f0f0')  # Fond clair
        
        # Positionnement des nœuds
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent
        
        # Couleurs des nœuds et arêtes
        node_colors = ['green' if sommet in chemin else 'lightblue' for sommet in self.sommets]
        path_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)] if len(chemin) > 1 else []
        edge_colors = ['red' if (u, v) in path_edges else 'gray' for u, v in G.edges()]
        edge_widths = [3 if (u, v) in path_edges else 1 for u, v in G.edges()]

        # Dessin du graphe
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=node_colors, 
            node_size=800,
            ax=ax
        )
        nx.draw_networkx_edges(
            G, pos, 
            edge_color=edge_colors,
            width=edge_widths,
            arrows=True,
            arrowstyle='->',
            arrowsize=20,
            ax=ax
        )
        nx.draw_networkx_labels(
            G, pos, 
            font_size=12,
            font_weight="bold",
            ax=ax
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
        
        # Ajouter le titre avec les informations
        if chemin:
            distance = 0
            for i in range(len(chemin) - 1):
                u, v = chemin[i], chemin[i+1]
                distance += G[u][v]['weight']
            
            title = (
                f"Chemin le plus court: {' → '.join(chemin)}\n"
                f"Distance totale: {distance}"
            )
        else:
            title = f"Aucun chemin trouvé entre {self.start} et {self.end}"
        
        ax.set_title(title, fontsize=14, pad=15)
        ax.set_axis_off()

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        self.canvas_widget = canvas
        canvas.get_tk_widget().pack(fill="both", expand=True)
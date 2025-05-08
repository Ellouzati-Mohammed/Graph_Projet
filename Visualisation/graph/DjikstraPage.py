# gui/pages/frame/algos/dijkstra_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Djikstra import djikstra  # Assurez-vous que le chemin d'import est correct
from data.graph_data import graph  # Adaptez selon votre structure

class DijkstraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None  # Pour stocker les données reçues
        self.sommets = []
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)
        self.menu_source = None
        self.menu_dest = None
        self.visualiser_djikstra_graphe()

    def set_data(self, data):
        """Méthode pour recevoir les données à visualiser (liste d'arêtes)"""
        self.data = data
        self.afficher_graphe_depuis_data()

    def update_controls(self):
        # Nettoyer les anciens menus
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        if not self.sommets:
            return
        tk.Label(self.controls_frame, text="Source :").pack(side=tk.LEFT, padx=5)
        self.menu_source = tk.OptionMenu(self.controls_frame, self.source_var, *self.sommets, command=self.on_selection_change)
        self.menu_source.pack(side=tk.LEFT, padx=5)
        tk.Label(self.controls_frame, text="Destination :").pack(side=tk.LEFT, padx=5)
        self.menu_dest = tk.OptionMenu(self.controls_frame, self.dest_var, *self.sommets, command=self.on_selection_change)
        self.menu_dest.pack(side=tk.LEFT, padx=5)

    def on_selection_change(self, _=None):
        self.afficher_graphe_depuis_data()

    def afficher_graphe_depuis_data(self):
        if not self.data:
            return
        # Extraire les sommets
        self.sommets = list(sorted(set([u for u, v, w in self.data] + [v for u, v, w in self.data])))
        n = len(self.sommets)
        sommet_index = {s: i for i, s in enumerate(self.sommets)}
        # Créer la matrice d'adjacence
        matrice_adjacence = [[float('inf')] * n for _ in range(n)]
        for u, v, w in self.data:
            i, j = sommet_index[u], sommet_index[v]
            matrice_adjacence[i][j] = w
        for i in range(n):
            matrice_adjacence[i][i] = 0
        # Mettre à jour les menus déroulants
        self.update_controls()
        # Choisir départ/arrivée (par défaut premier et dernier, sinon valeur sélectionnée)
        debut = self.source_var.get() if self.source_var.get() in self.sommets else self.sommets[0]
        depart = self.dest_var.get() if self.dest_var.get() in self.sommets else self.sommets[-1]
        self.source_var.set(debut)
        self.dest_var.set(depart)
        # Appliquer Dijkstra
        try:
            chemin = djikstra(self.sommets, matrice_adjacence, debut, depart)
        except Exception as e:
            print(f"Erreur Dijkstra: {e}")
            chemin = []
        # Créer le graphe
        G = nx.DiGraph()
        G.add_nodes_from(self.sommets)
        for u, v, w in self.data:
            G.add_edge(u, v, weight=w)
        # Nettoyage du canvas précédent
        if self.canvas_widget:
            self.canvas_widget.destroy()
        fig, ax = plt.subplots(figsize=(5, 5))
        pos = nx.spring_layout(G, seed=42)
        # Couleurs des nœuds et arêtes
        node_colors = ['green' if sommet in chemin else 'lightblue' for sommet in self.sommets]
        path_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)] if len(chemin) > 1 else []
        edge_colors = ['red' if (u, v) in path_edges else 'gray' for u, v in G.edges()]
        edge_widths = [2 if (u, v) in path_edges else 1 for u, v in G.edges()]
        # Dessin du graphe
        nx.draw(
            G, pos, ax=ax, with_labels=True,
            node_color=node_colors, 
            edge_color=edge_colors,
            width=edge_widths,
            node_size=300,
            font_size=9,
            font_weight="bold",
            arrows=True
        )
        # Affichage des poids des arêtes
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=edge_labels,
            ax=ax,
            font_color='red',
            font_size=7
        )
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def visualiser_djikstra_graphe(self):
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        # Sélection des nœuds de départ et d'arrivée (exemple: premier et dernier)
        debut = sommets[0]
        depart = sommets[-1]

        # Calcul du chemin avec Dijkstra
        try:
            chemin = djikstra(sommets, matrice_adjacence, debut, depart)
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

        fig, ax = plt.subplots(figsize=(5, 5))
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent

        # Couleurs des nœuds et arêtes
        node_colors = ['green' if sommet in chemin else 'lightblue' for sommet in sommets]
        path_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)] if len(chemin) > 1 else []
        edge_colors = ['red' if (u, v) in path_edges else 'gray' for u, v in G.edges()]
        edge_widths = [2 if (u, v) in path_edges else 1 for u, v in G.edges()]

        # Dessin du graphe
        nx.draw(
            G, pos, ax=ax, with_labels=True,
            node_color=node_colors, 
            edge_color=edge_colors,
            width=edge_widths,
            node_size=300,
            font_size=9,
            font_weight="bold",
            arrows=True
        )

        # Affichage des poids des arêtes
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=edge_labels,
            ax=ax,
            font_color='red',
            font_size=7
        )

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
# gui/pages/frame/algos/welsh_powell_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Welsh_Powell import Welsh_Powell  # adapte l'import selon ton arborescence
from data.graph_data import graph  # idem ici selon ta structure
from tkinter import ttk

class WelshPowellPage(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.canvas_widget = None
        
        # Créer un cadre principal avec padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Bouton de retour en haut à droite
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
       

        # Titre informatif
        num_colors = self.data['num_colors']
        title_label = ttk.Label(
            main_frame,
            text=f"Coloration de graphe (Welsh-Powell) - {num_colors} couleurs utilisées",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Cadre pour la visualisation avec bordure
        viz_frame = ttk.LabelFrame(main_frame, text="Visualisation du graphe")
        viz_frame.pack(fill="both", expand=True)
        
        # Créer un cadre interne pour le canvas
        canvas_frame = ttk.Frame(viz_frame)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mettre à jour la visualisation immédiatement
        self.create_graph_visualization(canvas_frame)

    def return_to_input(self):
        """Retourne à la page d'entrée"""
        if self.controller:
            self.controller.change_frame("InputGraphPage")

    # ... (le reste du code reste inchangé)

    def create_graph_visualization(self, parent_frame):
        """Crée la visualisation du graphe avec les sommets colorés"""
        sommets = self.data['sommets']
        matrice = self.data['matrice']
        colored_vertices = self.data['colored_vertices']
        
        # Créer le graphe
        G = nx.Graph()
        G.add_nodes_from(sommets)
        
        # Ajouter les arêtes
        for i in range(len(sommets)):
            for j in range(i + 1, len(sommets)):
                if matrice[i][j] > 0:
                    G.add_edge(sommets[i], sommets[j])
        
        # Créer la carte de couleurs
        color_map = []
        color_palette = plt.cm.tab10.colors  # Palette de 10 couleurs
        color_index_map = {}  # Map: couleur RGB -> indice numérique
        next_color_index = 0  # Prochain indice de couleur disponible
        
        for sommet in sommets:
            index = sommets.index(sommet)
            color_code = None
            for colored in colored_vertices:
                if colored[0] == index:
                    color_code = colored[1]
                    break
            
            # Trouver ou créer l'indice de couleur
            if color_code not in color_index_map:
                color_index_map[color_code] = next_color_index
                next_color_index += 1
            
            # Obtenir la couleur RGB correspondante
            color_idx = color_index_map[color_code] % len(color_palette)
            color_rgb = color_palette[color_idx]
            color_map.append(color_rgb)
        
        # Créer la figure
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f0f0f0')  # Fond clair pour correspondre au thème
        
        # Positionnement des nœuds
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent
        
        # Dessiner le graphe
        nx.draw_networkx(
            G, 
            pos, 
            ax=ax,
            node_color=color_map, 
            node_size=800,
            edge_color="gray",
            width=1.5,
            font_size=10,
            font_weight="bold",
            with_labels=True
        )
        
        # Ajouter une légende simplifiée
        legend_handles = []
        for color_idx in range(next_color_index):
            # Obtenir la couleur RGB correspondante
            color_rgb = color_palette[color_idx % len(color_palette)]
        
        # Titre
        ax.set_title("Coloration des sommets", fontsize=12, pad=15)
        
        # Désactiver les axes
        ax.set_axis_off()
        
        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Stocker une référence pour éviter la destruction par le garbage collector
        self.canvas_widget = canvas
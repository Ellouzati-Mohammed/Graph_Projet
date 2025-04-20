import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from data.graph_data import graph 
from algorithms.graph.Welsh_Powell import Welsh_Powell

class VisualisationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        

    def visualiser_graphe(self):        
        graphe_data = graph.get_graphe()
        sommets=graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        oriente=graphe_data["oriente"]

        G = nx.DiGraph() if oriente else nx.Graph()
        
        G.add_nodes_from(sommets)
        
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice_adjacence[i][j]
                if poids > 0:  
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        # Supprimer le canvas précédent s'il existe
        if hasattr(self, 'canvas_widget'):
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(4, 4))
        pos = nx.spring_layout(G, seed=42) 
        
        nx.draw(G, pos, ax=ax, with_labels=True, 
               node_size=200, 
               node_color="lightblue", 
               font_size=8, 
               font_weight="bold")

        edge_labels = nx.get_edge_attributes(G, "weight")
        
        nx.draw_networkx_edge_labels(G, pos, ax=ax, 
                                    edge_labels=edge_labels,
                                    font_color='red')
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
    

    def visualiser_Wech_Powell_graphe(self):        
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        # Appeler la fonction Welsh_Powell et récupérer les résultats
        colored_sommets = Welsh_Powell(sommets, matrice_adjacence)
 
        
        # Créer un dictionnaire de couleurs pour chaque sommet
        color_map = {sommet: color for sommet, color in colored_sommets}
        print(color_map)
        # Créer le graphe NetworkX
        G = nx.Graph()  # ou nx.DiGraph() si c'est un graphe orienté
        
        G.add_nodes_from(sommets)
        
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice_adjacence[i][j]
                if poids > 0:  
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        # Supprimer le canvas précédent s'il existe
        if hasattr(self, 'canvas_widget'):
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(4, 4))
        pos = nx.spring_layout(G, seed=42) 


        node_colors = []

        for index,sommet in enumerate(sommets):
            color = color_map.get(index)  #
            print(color)
            node_colors.append(color)

        
        nx.draw(G, pos, ax=ax, with_labels=True, 
                node_size=200, 
                node_color=node_colors,  # Utilisation des couleurs récupérées
                font_size=8, 
                font_weight="bold")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, ax=ax, 
                                    edge_labels=edge_labels,
                                    font_color='red',
                                    font_size=7)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

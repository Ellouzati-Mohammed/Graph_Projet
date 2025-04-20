# gui/pages/frame/algos/welsh_powell_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Welsh_Powell import Welsh_Powell  # adapte l'import selon ton arborescence
from data.graph_data import graph  # idem ici selon ta structure

class WelshPowellPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.visualiser_Wech_Powell_graphe()

    def visualiser_Wech_Powell_graphe(self):
        graphe_data = graph.get_graphe()
        sommets = graphe_data['sommets']
        matrice_adjacence = graphe_data['matrice']
        
        colored_sommets = Welsh_Powell(sommets, matrice_adjacence)
        color_map = {sommet: color for sommet, color in colored_sommets}
        print("Coloration:", color_map)

        G = nx.Graph()
        G.add_nodes_from(sommets)

        for i in range(len(sommets)):
            for j in range(len(sommets)):
                poids = matrice_adjacence[i][j]
                if poids > 0:
                    G.add_edge(sommets[i], sommets[j], weight=poids)

        if self.canvas_widget:
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 5))
        pos = nx.spring_layout(G, seed=42)

        node_colors = []
        for index, sommet in enumerate(sommets):
            node_colors.append(color_map.get(index, "gray"))  # couleur par défaut

        nx.draw(G, pos, ax=ax, with_labels=True,
                node_size=300,
                node_color=node_colors,
                font_size=9,
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

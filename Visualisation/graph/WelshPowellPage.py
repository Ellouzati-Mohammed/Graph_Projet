# gui/pages/frame/algos/welsh_powell_page.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Welsh_Powell import Welsh_Powell  # adapte l'import selon ton arborescence
from data.graph_data import graph  # idem ici selon ta structure
class WelshPowellPage(tk.Frame):
    def __init__(self, parent, controller, graph_data):
        super().__init__(parent)
        self.controller = controller
        self.graph_data = graph_data
        self.canvas_widget = None
        
        # Add a back button
        back_button = ttk.Button(self, text="Retour", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)
        
        # Visualization will be updated by parent
        self.viz_frame = ttk.Frame(self)
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
    def reset_graph(self):
        """Retourne à la page d'entrée pour charger un nouveau graphe"""
        self.controller.change_frame("input_welsh_powell")
    def go_back(self):
        """Return to input page"""
        self.controller.change_frame("input_welsh_powell")
    
    def update_visualization(self, colored_vertices):
        """Update the visualization with colored vertices"""
        if self.canvas_widget:
            self.canvas_widget.destroy()
        
        sommets = self.graph_data['sommets']
        matrice = self.graph_data['matrice']
        
        G = nx.Graph()
        G.add_nodes_from(sommets)
        
        # Add edges
        for i in range(len(sommets)):
            for j in range(len(sommets)):
                if matrice[i][j] > 0 and i < j:
                    G.add_edge(sommets[i], sommets[j])
        
        # Create color map
        color_map = []
        for sommet in sommets:
            index = sommets.index(sommet)
            for colored in colored_vertices:
                if colored[0] == index:
                    color_map.append(colored[1])
                    break
        
        fig = plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=800, font_weight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
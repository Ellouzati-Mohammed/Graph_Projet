import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.FordFulkerson import fordFulkerson
from data.graph_data import graph 

class FordFulkersonPage(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = data
        self.visualiser_ford_fulkerson()

    def visualiser_ford_fulkerson(self):
        sommets = self.data['sommets']
        matrice = self.data['matrice']
        source = self.data['source']
        sink = self.data['sink']
        try:
            from algorithms.graph.FordFulkerson import fordFulkerson
            max_flow, residual_graph = fordFulkerson(sommets, matrice, source, sink)
        except Exception as e:
            max_flow = 0
            residual_graph = {}
            print(f"Erreur: {e}")

        # Création du graphe orienté
        G = nx.DiGraph()
        G.add_nodes_from(sommets)
        n = len(sommets)
        for i in range(n):
            for j in range(n):
                if matrice[i][j] > 0:
                    u, v = sommets[i], sommets[j]
                    # flot = capacité initiale - capacité résiduelle
                    res_cap = residual_graph[u][v] if u in residual_graph and v in residual_graph[u] else 0
                    flow = matrice[i][j] - res_cap
                    flow = max(0, flow)
                    G.add_edge(u, v, capacity=matrice[i][j], flow=flow)

        # Nettoyage du canvas précédent
        if self.canvas_widget:
            self.canvas_widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)

        # Style des arêtes :
        edge_colors = []
        edge_widths = []
        for u, v, data in G.edges(data=True):
            if data['flow'] == max_flow and max_flow > 0:
                edge_colors.append('green')
                edge_widths.append(3)
            elif data['flow'] > 0:
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
        edge_labels = {
            (u, v): f"{data['flow']}/{data['capacity']}"
            for u, v, data in G.edges(data=True)
        }
        
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
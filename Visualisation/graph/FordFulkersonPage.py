import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class FordFulkersonPage(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.viz_frame = tk.Frame(self)  # Frame principal pour la visualisation
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
        self.visualiser_ford_fulkerson()
        
    def visualiser_ford_fulkerson(self):
        """Calcule le flot maximum et affiche la visualisation complète"""
        sommets = self.data['sommets']
        matrice = np.array(self.data['matrice'])  # Convertir en array numpy
        source = self.data['source']
        sink = self.data['sink']
        
        # Calcul du flot maximum avec Ford-Fulkerson
        max_flow, flow_matrix = fordFulkerson(
            sommets, 
            matrice.tolist(),  # Reconversion en liste
            source, 
            sink
        )
        
        # Appel de la visualisation complète
        self.visualize_network(sommets, matrice, flow_matrix, max_flow)

    def visualize_network(self, nodes, capacity_matrix, flow_matrix, max_flow):
        """Visualise le réseau avec capacités, flots, légende et tableau de détails"""
        # Nettoyer la frame précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer le graphe orienté
        G = nx.DiGraph()
        G.add_nodes_from(nodes)

        # Ajouter les arêtes avec capacités et flots
        edge_labels = {}
        edge_colors = []

        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if capacity_matrix[i][j] > 0:
                    G.add_edge(nodes[i], nodes[j])
                    flow = flow_matrix[i][j]
                    capacity = capacity_matrix[i][j]

                    # Formatage du label des arêtes
                    edge_labels[(nodes[i], nodes[j])] = f"{flow}/{capacity}"

                    # Codage couleur
                    if flow == 0:
                        edge_colors.append("#cccccc")  # Gris - pas de flot
                    elif flow == capacity:
                        edge_colors.append("#ff6b6b")  # Rouge - saturé
                    else:
                        edge_colors.append("#51cf66")  # Vert - flot partiel

        # Création de la figure
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Positionnement des nœuds
        pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

        # Dessin des nœuds
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            node_size=1500,
            node_color="#339af0",
            alpha=0.9,
            linewidths=2,
            edgecolors="#1864ab",
        )

        # Dessin des labels
        nx.draw_networkx_labels(
            G, pos, ax=ax, font_size=12, font_weight="bold", font_color="white"
        )

        # Dessin des arêtes
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edge_color=edge_colors,
            width=3,
            arrows=True,
            arrowsize=25,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.1",
        )

        # Labels des arêtes
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            ax=ax,
            font_size=10,
            font_color="#343a40",
            bbox=dict(
                facecolor="white", edgecolor="none", alpha=0.8, boxstyle="round,pad=0.3"
            ),
        )

        # Titre
        ax.set_title(
            f"Réseau de flot - Flot maximum: {max_flow}",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )
        ax.axis("off")
        plt.tight_layout()

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Ajout du panneau d'information
        info_frame = ttk.Frame(self.viz_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        # Affichage du flot maximum
        ttk.Label(
            info_frame,
            text=f"Flot maximum: {max_flow}",
            font=("Arial", 12, "bold"),
            foreground="#2b8a3e",
        ).pack(side=tk.LEFT, padx=10)

        # Légende
        legend_frame = ttk.Frame(info_frame)
        legend_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(legend_frame, text="Légende:").pack(anchor="w")
        ttk.Label(legend_frame, text="• Gris: Pas de flot", foreground="#868e96").pack(anchor="w")
        ttk.Label(legend_frame, text="• Vert: Flot partiel", foreground="#51cf66").pack(anchor="w")
        ttk.Label(legend_frame, text="• Rouge: Flot maximal", foreground="#ff6b6b").pack(anchor="w")

        # Tableau de détails des flots
        details_frame = ttk.Frame(self.viz_frame)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        columns = ("Source", "Destination", "Flot", "Capacité", "Saturation")
        tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=6)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Remplissage du tableau
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if capacity_matrix[i][j] > 0:
                    flow = flow_matrix[i][j]
                    cap = capacity_matrix[i][j]
                    saturation = f"{(flow/cap)*100:.1f}%" if cap > 0 else "0%"
                    tree.insert("", "end", values=(nodes[i], nodes[j], flow, cap, saturation))

        # Ajout de la scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)


# Algorithme Ford-Fulkerson (à conserver dans un fichier séparé ou dans le même)
def fordFulkerson(nodes, capacity_matrix, source, sink):
    """Implémentation de l'algorithme Ford-Fulkerson avec BFS (Edmonds-Karp)"""
    n = len(nodes)
    source_idx = nodes.index(source)
    sink_idx = nodes.index(sink)

    flow_matrix = [[0] * n for _ in range(n)]
    residual_graph = [[capacity_matrix[i][j] for j in range(n)] for i in range(n)]
    parent = [-1] * n
    max_flow = 0

    def bfs(res_graph, s, t, parent):
        visited = [False] * n
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for v in range(n):
                if not visited[v] and res_graph[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == t:
                        return True
        return False

    while bfs(residual_graph, source_idx, sink_idx, parent):
        path_flow = float("Inf")
        s = sink_idx

        while s != source_idx:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        v = sink_idx
        while v != source_idx:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            flow_matrix[u][v] += path_flow
            v = u

        max_flow += path_flow

    return max_flow, flow_matrix
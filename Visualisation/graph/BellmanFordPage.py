import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.BellmanFord import bellmanFord
from data.graph_data import graph 

class BellmanFordPage(tk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = data
        self.graph_data = {
            "nodes": [],
            "start": "",
            "end": ""
        }
        self.visualiser_bellman_ford_graphe()

    def bellman_ford(self, nodes, graph, source):
        """Implementation of Bellman-Ford algorithm"""
        n = len(nodes)
        src_idx = nodes.index(source)

        # Initialize distances and predecessors
        distances = [float("inf")] * n
        predecessors = [-1] * n
        distances[src_idx] = 0

        # Relax all edges |V| - 1 times
        for _ in range(n - 1):
            for u in range(n):
                for v in range(n):
                    if graph[u][v] != 0:  # There's an edge from u to v
                        if distances[u] + graph[u][v] < distances[v]:
                            distances[v] = distances[u] + graph[u][v]
                            predecessors[v] = u

        # Check for negative-weight cycles
        for u in range(n):
            for v in range(n):
                if graph[u][v] != 0:  # There's an edge from u to v
                    if distances[u] + graph[u][v] < distances[v]:
                        return None, None  # Negative cycle detected

        return distances, predecessors

    def reconstruct_path(self, predecessors, end_node):
        """Reconstruct the shortest path from predecessors array"""
        nodes = self.graph_data["nodes"]
        path = []
        current = end_node
        while current != -1:
            path.insert(0, current)
            current_idx = nodes.index(current)
            pred_idx = predecessors[current_idx]
            if pred_idx == -1:
                break
            current = nodes[pred_idx]
        return path

    def visualiser_bellman_ford_graphe(self):
        # Get graph data
        if self.data:
            sommets = self.data['sommets']
            matrice_adjacence = self.data['matrice']
            debut = self.data['start']
            fin = self.data['end']
        else:
            graphe_data = graph.get_graphe()
            sommets = graphe_data['sommets']
            matrice_adjacence = graphe_data['matrice']
            debut = sommets[0]
            fin = sommets[-1]

        # Store in graph_data
        self.graph_data = {
            "nodes": sommets,
            "start": debut,
            "end": fin
        }

        # Calculate distances and predecessors
        distances, predecessors = self.bellman_ford(sommets, matrice_adjacence, debut)
        
        # Clear previous visualization
        for widget in self.winfo_children():
            widget.destroy()

        # Create main visualization frame
        viz_frame = ttk.Frame(self)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create directed graph
        G = nx.DiGraph()
        G.add_nodes_from(sommets)

        # Add edges with weights
        edge_labels = {}
        edge_colors = []
        edge_widths = []

        # Check if valid path exists
        end_idx = sommets.index(fin)
        has_path = distances and distances[end_idx] != float("inf")

        # Reconstruct shortest path edges
        path_edges = set()
        if has_path:
            path_nodes = self.reconstruct_path(predecessors, fin)
            for i in range(len(path_nodes) - 1):
                path_edges.add((path_nodes[i], path_nodes[i + 1]))

        for i in range(len(sommets)):
            for j in range(len(sommets)):
                if matrice_adjacence[i][j] != 0:
                    G.add_edge(sommets[i], sommets[j])
                    edge_labels[(sommets[i], sommets[j])] = matrice_adjacence[i][j]

                    # Highlight edges in shortest path
                    if (sommets[i], sommets[j]) in path_edges:
                        edge_colors.append("#ff6b6b")  # Red for path edges
                        edge_widths.append(3)
                    else:
                        edge_colors.append("#cccccc")  # Gray for other edges
                        edge_widths.append(1)

        # Create figure with modern layout
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Node positioning
        pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

        # Draw nodes with distance information
        node_colors = []
        node_labels = {}
        for i, node in enumerate(sommets):
            if distances[i] == float("inf"):
                node_labels[node] = f"{node}\n∞"
                node_colors.append("#adb5bd")  # Gray for unreachable
            else:
                node_labels[node] = f"{node}\n{distances[i]}"
                if node == debut:
                    node_colors.append("#51cf66")  # Green for start
                elif node == fin:
                    node_colors.append("#ff6b6b")  # Red for end
                else:
                    node_colors.append("#339af0")  # Blue for intermediate

        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            node_size=1500,
            node_color=node_colors,
            alpha=0.9,
            linewidths=2,
            edgecolors="#1864ab",
        )

        # Draw node labels
        nx.draw_networkx_labels(
            G,
            pos,
            ax=ax,
            labels=node_labels,
            font_size=10,
            font_weight="bold",
            font_color="white",
        )

        # Draw edges with styling
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edge_color=edge_colors,
            width=edge_widths,
            arrows=True,
            arrowsize=20,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.1",
        )

        # Edge weight labels
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

        # Title with result information
        title = "Algorithme de Bellman-Ford"
        if has_path:
            title += f"\nDistance de {debut} à {fin}: {distances[end_idx]}"
        else:
            title += "\nAucun chemin trouvé ou cycle négatif détecté"
        ax.set_title(title, fontsize=12, fontweight="bold", pad=20)

        ax.axis("off")
        plt.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add information panel
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        # Legend section
        legend_frame = ttk.LabelFrame(info_frame, text="Légende")
        legend_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        ttk.Label(
            legend_frame, 
            text="• Vert: Noeud de départ", 
            foreground="#51cf66",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Label(
            legend_frame, 
            text="• Rouge: Noeud d'arrivée", 
            foreground="#ff6b6b",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Label(
            legend_frame, 
            text="• Bleu: Noeuds intermédiaires", 
            foreground="#339af0",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Label(
            legend_frame, 
            text="• Gris: Noeuds inaccessibles", 
            foreground="#adb5bd",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        
        ttk.Label(
            legend_frame, 
            text="• Rouge: Arêtes du chemin", 
            foreground="#ff6b6b",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=2)

        # Path info section
        if has_path:
            path_frame = ttk.LabelFrame(info_frame, text="Chemin optimal")
            path_frame.pack(side=tk.RIGHT, padx=10, fill=tk.X, expand=True)

            path = self.reconstruct_path(predecessors, fin)
            path_str = " → ".join(path)
            ttk.Label(
                path_frame,
                text=path_str,
                font=("Arial", 10, "bold"),
                foreground="#2b8a3e",
            ).pack(padx=5, pady=5)
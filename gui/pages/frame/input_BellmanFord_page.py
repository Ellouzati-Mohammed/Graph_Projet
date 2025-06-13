import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from Visualisation.graph.BellmanFordPage import BellmanFordPage

class InputBellmanFordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.graph_data = {"nodes": [], "edges": [], "start": "", "end": ""}
        self.canvas_widget = None
        self.create_widgets()
        self.style_widgets()

    def style_widgets(self):
        """Apply modern styling to widgets"""
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure(
            "Accent.TButton",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#4a6baf",
        )
        style.configure(
            "TLabelframe", background="#f0f0f0", relief="groove", borderwidth=2
        )
        style.configure(
            "TLabelframe.Label", background="#f0f0f0", font=("Arial", 10, "bold")
        )
        style.configure("TEntry", padding=5)
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        self.configure(background="#f0f0f0")

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel for input controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 20))

        # Right panel for visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True)

        # Title
        title_frame = ttk.Frame(left_panel)
        title_frame.pack(fill="x", pady=(0, 15))
        title_label = ttk.Label(
            title_frame,
            text="Algorithme de Bellman-Ford",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()
        subtitle_label = ttk.Label(
            title_frame,
            text="Calcul du plus court chemin avec poids négatifs",
            font=("Arial", 10),
            foreground="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 10))

        # Graph info display
        self.graph_info_frame = ttk.LabelFrame(
            left_panel, text="Informations du graphe"
        )
        self.graph_info_frame.pack(fill="x", pady=5)
        self.graph_info_label = ttk.Label(
            self.graph_info_frame, text="Aucun graphe chargé", justify="left"
        )
        self.graph_info_label.pack(padx=5, pady=5)

        # Import section
        import_frame = ttk.LabelFrame(left_panel, text="Importation des données")
        import_frame.pack(fill="x", pady=10)

        btn_frame = ttk.Frame(import_frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            btn_frame,
            text="Import JSON",
            command=self.import_json,
            style="Accent.TButton",
        ).pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(
            btn_frame,
            text="Import CSV",
            command=self.import_csv,
            style="Accent.TButton",
        ).pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(
            btn_frame,
            text="Saisie manuelle",
            command=self.show_manual_input,
            style="Accent.TButton",
        ).pack(side="left", padx=5, fill="x", expand=True)

        # Info/help section
        info_frame = ttk.LabelFrame(left_panel, text="Instructions")
        info_frame.pack(fill="x", pady=5)
        info_text = (
            "1. Importez un graphe depuis un fichier (JSON/CSV)\n"
            "   ou saisissez les données manuellement\n\n"
            "2. Le graphe doit contenir :\n"
            "   - Des noeuds (noms uniques)\n"
            "   - Des arêtes avec poids (noeud1,noeud2,poids)\n"
            "   - Un sommet de départ et d'arrivée\n\n"
            "3. Lancez l'algorithme pour calculer\n"
            "   le plus court chemin dans le graphe"
        )
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)

        # Navigation buttons
        nav_frame = ttk.Frame(left_panel)
        nav_frame.pack(fill="x", pady=(20, 0))

        ttk.Button(nav_frame, text="Réinitialiser", command=self.reset_data).pack(
            side="left", padx=5, fill="x", expand=True
        )
        ttk.Button(
            nav_frame,
            text="Retour au menu",
            command=lambda: self.controller.change_frame("menu"),
        ).pack(side="left", padx=5, fill="x", expand=True)
        self.run_button = ttk.Button(
            nav_frame,
            text="Lancer l'algorithme",
            command=self.run_algorithm,
            state="disabled",
            style="Accent.TButton",
        )
        self.run_button.pack(side="left", padx=5, fill="x", expand=True)

        # Visualization panel
        self.viz_frame = ttk.LabelFrame(right_panel, text="Visualisation du graphe")
        self.viz_frame.pack(fill="both", expand=True)

        # Placeholder for graph visualization
        placeholder = ttk.Label(
            self.viz_frame,
            text="Le graphe s'affichera ici après exécution de l'algorithme",
            justify="center",
            font=("Arial", 10, "italic"),
            foreground="#7f8c8d",
        )
        placeholder.pack(expand=True, fill="both")

        # Status bar
        self.status_bar = ttk.Label(
            self,
            text="Prêt",
            relief="sunken",
            anchor="w",
            font=("Arial", 9),
            foreground="#2c3e50",
        )
        self.status_bar.pack(side="bottom", fill="x")

    def update_status(self, message):
        """Update the status bar message"""
        self.status_bar.config(text=message)
        self.update_idletasks()

    def update_graph_info(self):
        """Update the graph information display"""
        if not self.graph_data["nodes"]:
            info_text = "Aucun graphe chargé"
        else:
            info_text = (
                f"• Nombre de noeuds: {len(self.graph_data['nodes'])}\n"
                f"• Nombre d'arêtes: {len(self.graph_data['edges'])}\n"
                f"• Départ: {self.graph_data['start']}\n"
                f"• Arrivée: {self.graph_data['end']}"
            )

        self.graph_info_label.config(text=info_text)

    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                required = ["nodes", "edges", "start", "end"]
                if not all(k in data for k in required):
                    raise ValueError("Format JSON invalide")

                self.graph_data = data
                self.validate_data()
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès", f"Graphe importé avec {len(data['nodes'])} noeuds"
                )
                self.update_status(f"Graphe JSON chargé: {len(data['nodes'])} noeuds")

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'import: {str(e)}")
                self.update_status("Erreur lors de l'importation JSON")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline="") as f:
                    reader = csv.reader(f)
                    data = list(reader)

                if len(data) < 2:
                    raise ValueError("Fichier CSV incomplet")

                self.graph_data = {
                    "nodes": [str(n) for n in data[0]],
                    "start": str(data[1][0]),
                    "end": str(data[1][1]),
                    "edges": [
                        [row[0], row[1], float(row[2])]
                        for row in data[2:]
                        if len(row) >= 3
                    ],
                }

                self.validate_data()
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès",
                    f"Graphe importé avec {len(self.graph_data['nodes'])} noeuds",
                )
                self.update_status(
                    f"Graphe CSV chargé: {len(self.graph_data['nodes'])} noeuds"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'import: {str(e)}")
                self.update_status("Erreur lors de l'importation CSV")

    def show_manual_input(self):
        """Show manual input dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle du graphe")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f0f0")

        # Main container
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nodes input
        nodes_frame = ttk.LabelFrame(
            main_frame, text="Noeuds (séparés par des virgules)"
        )
        nodes_frame.pack(fill="x", pady=5)
        nodes_entry = ttk.Entry(nodes_frame)
        nodes_entry.pack(fill="x", padx=5, pady=5)

        # Start and End nodes
        start_end_frame = ttk.Frame(main_frame)
        start_end_frame.pack(fill="x", pady=5)

        ttk.Label(start_end_frame, text="Départ:").pack(side="left", padx=5)
        start_entry = ttk.Entry(start_end_frame, width=20)
        start_entry.pack(side="left", padx=5)

        ttk.Label(start_end_frame, text="Arrivée:").pack(side="left", padx=5)
        end_entry = ttk.Entry(start_end_frame, width=20)
        end_entry.pack(side="left", padx=5)

        # Edges input
        edges_frame = ttk.LabelFrame(
            main_frame, text="Arêtes (une par ligne, format: noeud1,noeud2,poids)"
        )
        edges_frame.pack(fill="both", expand=True, pady=5)

        edges_text = tk.Text(edges_frame, height=10, width=40)
        edges_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(
            side="left", padx=5, fill="x", expand=True
        )

        ttk.Button(
            button_frame,
            text="Valider",
            command=lambda: self.validate_manual_input(
                dialog,
                nodes_entry.get(),
                start_entry.get(),
                end_entry.get(),
                edges_text.get("1.0", "end-1c"),
            ),
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def validate_manual_input(self, dialog, nodes_str, start, end, edges_str):
        """Validate manual input data"""
        try:
            nodes = [n.strip() for n in nodes_str.split(",") if n.strip()]
            if not nodes:
                raise ValueError("Veuillez saisir au moins un noeud")

            if not start or not end:
                raise ValueError("Le départ et l'arrivée doivent être spécifiés")

            if start not in nodes:
                raise ValueError("Le départ doit être dans la liste des noeuds")

            if end not in nodes:
                raise ValueError("L'arrivée doit être dans la liste des noeuds")

            edges = []
            for line in edges_str.split("\n"):
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        raise ValueError(f"Format d'arête invalide: {line}")
                    if parts[0] not in nodes or parts[1] not in nodes:
                        raise ValueError(f"Arête {line} référence un noeud inexistant")
                    try:
                        weight = float(parts[2])
                        edges.append([parts[0], parts[1], weight])
                    except ValueError:
                        raise ValueError(f"Poids doit être un nombre pour {line}")

            self.graph_data = {
                "nodes": nodes,
                "edges": edges,
                "start": start,
                "end": end,
            }

            self.validate_data()
            self.update_graph_info()
            self.run_button.config(state="normal")
            dialog.destroy()
            messagebox.showinfo(
                "Succès", f"Graphe créé avec {len(nodes)} noeuds et {len(edges)} arêtes"
            )
            self.update_status(
                f"Graphe manuel créé: {len(nodes)} noeuds, {len(edges)} arêtes"
            )

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=dialog)
            self.update_status("Erreur dans la saisie manuelle")

    def validate_data(self):
        """Validate graph data"""
        if not self.graph_data["nodes"]:
            raise ValueError("Aucun noeud spécifié")

        if self.graph_data["start"] not in self.graph_data["nodes"]:
            raise ValueError("Départ non trouvé dans les noeuds")

        if self.graph_data["end"] not in self.graph_data["nodes"]:
            raise ValueError("Arrivée non trouvée dans les noeuds")

        for edge in self.graph_data["edges"]:
            if (
                edge[0] not in self.graph_data["nodes"]
                or edge[1] not in self.graph_data["nodes"]
            ):
                raise ValueError(f"Arête {edge} référence un noeud inexistant")
            if edge[0] == edge[1]:
                raise ValueError(f"Boucle détectée sur le noeud {edge[0]}")

    def reset_data(self):
        """Reset all graph data"""
        self.graph_data = {"nodes": [], "edges": [], "start": "", "end": ""}

        # Update graph info display
        self.update_graph_info()

        # Disable run button
        self.run_button.config(state="disabled")

        # Clear visualization
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None

        # Add placeholder back
        placeholder = ttk.Label(
            self.viz_frame,
            text="Le graphe s'affichera ici après exécution de l'algorithme",
            justify="center",
            font=("Arial", 10, "italic"),
            foreground="#7f8c8d",
        )
        placeholder.pack(expand=True, fill="both")

        messagebox.showinfo(
            "Réinitialisation", "Toutes les données ont été réinitialisées"
        )
        self.update_status("Prêt - Données réinitialisées")

    def run_algorithm(self):
        """Run Bellman-Ford algorithm and visualize the result using BellmanFordPage"""
        if not self.graph_data["nodes"] or not self.graph_data["edges"]:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord importer ou saisir les données du graphe"
            )
            return

        try:
            self.update_status("Exécution de l'algorithme de Bellman-Ford...")

            # Supprimer le placeholder
            if hasattr(self, 'placeholder'):
                self.placeholder.pack_forget()

            # Transform data to expected format
            nodes = self.graph_data["nodes"]
            n = len(nodes)
            matrice_adjacence = [[0] * n for _ in range(n)]
            node_index = {node: i for i, node in enumerate(nodes)}

            for u, v, weight in self.graph_data["edges"]:
                i, j = node_index[u], node_index[v]
                matrice_adjacence[i][j] = weight

            # Prepare data for BellmanFordPage
            data = {
                'sommets': nodes,
                'matrice': matrice_adjacence,
                'start': self.graph_data["start"],
                'end': self.graph_data["end"]
            }

            # Display the results using BellmanFordPage
            self.display_bellman_ford_results(data)

            self.update_status("Algorithme de Bellman-Ford exécuté avec succès")

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e))
            self.update_status("Erreur dans les données d'entrée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def display_bellman_ford_results(self, data):
        """Affiche les résultats avec la classe BellmanFordPage"""
        # Effacer la visualisation précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer un cadre conteneur pour BellmanFordPage
        container = ttk.Frame(self.viz_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialiser et afficher BellmanFordPage dans le conteneur
        bellman_ford_page = BellmanFordPage(container, data)
        bellman_ford_page.pack(fill="both", expand=True)

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
        path = []
        current = end_node
        while current != -1:
            path.insert(0, current)
            current_idx = self.graph_data["nodes"].index(current)
            pred_idx = predecessors[current_idx]
            if pred_idx == -1:
                break
            current = self.graph_data["nodes"][pred_idx]
        return path

    def visualize_graph(self, nodes, adjacency_matrix, distances, predecessors):
        """Visualize the graph with shortest path information"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create directed graph
        G = nx.DiGraph()
        G.add_nodes_from(nodes)

        # Add edges with weights
        edge_labels = {}
        edge_colors = []
        edge_widths = []

        # Determine if we have a valid path to highlight
        end_idx = nodes.index(self.graph_data["end"])
        has_path = distances[end_idx] != float("inf")

        # Reconstruct the shortest path edges
        path_edges = set()
        if has_path:
            path_nodes = self.reconstruct_path(predecessors, self.graph_data["end"])
            for i in range(len(path_nodes) - 1):
                path_edges.add((path_nodes[i], path_nodes[i + 1]))

        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if adjacency_matrix[i][j] != 0:
                    G.add_edge(nodes[i], nodes[j])
                    edge_labels[(nodes[i], nodes[j])] = adjacency_matrix[i][j]

                    # Highlight edges in the shortest path
                    if (nodes[i], nodes[j]) in path_edges:
                        edge_colors.append("#ff6b6b")  # Red for path edges
                        edge_widths.append(3)
                    else:
                        edge_colors.append("#cccccc")  # Gray for other edges
                        edge_widths.append(1)

        # Create figure with better layout
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Improved node positioning
        pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

        # Draw nodes with distance information
        node_colors = []
        node_labels = {}
        for i, node in enumerate(nodes):
            if distances[i] == float("inf"):
                node_labels[node] = f"{node}\n∞"
                node_colors.append("#adb5bd")  # Gray for unreachable nodes
            else:
                node_labels[node] = f"{node}\n{distances[i]}"
                if node == self.graph_data["start"]:
                    node_colors.append("#51cf66")  # Green for start node
                elif node == self.graph_data["end"]:
                    node_colors.append("#ff6b6b")  # Red for end node
                else:
                    node_colors.append("#339af0")  # Blue for other nodes

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

        # Draw node labels with distance information
        nx.draw_networkx_labels(
            G,
            pos,
            ax=ax,
            labels=node_labels,
            font_size=10,
            font_weight="bold",
            font_color="white",
        )

        # Draw edges with arrows and custom styling
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

        # Edge labels with weights
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

        # Title with better styling
        title = "Graphe avec plus courts chemins (Bellman-Ford)"
        if has_path:
            title += f"\nDistance de {self.graph_data['start']} à {self.graph_data['end']}: {distances[end_idx]}"
        ax.set_title(title, fontsize=12, fontweight="bold", pad=20)

        # Remove axes
        ax.axis("off")

        plt.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas_widget = canvas_widget

        # Add information panel below the graph
        info_frame = ttk.Frame(self.viz_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        # Legend
        legend_frame = ttk.Frame(info_frame)
        legend_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(legend_frame, text="Légende:").pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Vert: Noeud de départ", foreground="#51cf66"
        ).pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Rouge: Noeud d'arrivée", foreground="#ff6b6b"
        ).pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Bleu: Noeuds intermédiaires", foreground="#339af0"
        ).pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Gris: Noeuds inaccessibles", foreground="#adb5bd"
        ).pack(anchor="w")

        # Path info
        if has_path:
            path_frame = ttk.Frame(info_frame)
            path_frame.pack(side=tk.RIGHT, padx=10)

            path = self.reconstruct_path(predecessors, self.graph_data["end"])
            path_str = " → ".join(path)
            ttk.Label(
                path_frame,
                text=f"Chemin le plus court: {path_str}",
                font=("Arial", 10, "bold"),
                foreground="#2b8a3e",
            ).pack(anchor="e")

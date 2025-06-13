import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from collections import defaultdict
import math
import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DijkstraImporter:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.frame = ttk.LabelFrame(parent_frame, text="Importation des données")
        self.frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            self.frame,
            text="Import JSON",
            command=self.import_json,
            style="Accent.TButton",
        ).pack(side="left", padx=5, pady=5, fill="x", expand=True)

        ttk.Button(
            self.frame,
            text="Import CSV",
            command=self.import_csv,
            style="Accent.TButton",
        ).pack(side="left", padx=5, pady=5, fill="x", expand=True)

        ttk.Button(
            self.frame,
            text="Saisie manuelle",
            command=self.manual_input,
            style="Accent.TButton",
        ).pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                if "sommets" in data and "matrice" in data:
                    # Use the provided format directly
                    self.controller.set_graph_data(data["sommets"], data["matrice"])
                elif "nodes" in data and "edges" in data:
                    # Original conversion code
                    nodes = data["nodes"]
                    node_index = {node: idx for idx, node in enumerate(nodes)}
                    matrix = [[0] * len(nodes) for _ in range(len(nodes))]

                    for edge in data["edges"]:
                        i = node_index[edge["from"]]
                        j = node_index[edge["to"]]
                        matrix[i][j] = edge["weight"]

                    self.controller.set_graph_data(nodes, matrix)
                else:
                    messagebox.showerror(
                        "Erreur",
                        "Format JSON invalide. Doit contenir 'nodes' et 'edges' ou 'sommets' et 'matrice'",
                    )
            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Erreur lors de la lecture du fichier: {str(e)}"
                )

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline="") as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)

                # Check if the first row starts with empty or comma (CSV header)
                if data and data[0][0] == "" and len(data[0]) > 1:
                    # This is the format with node names in first row and column
                    nodes = data[0][
                        1:
                    ]  # Get node names from first row (excluding first empty cell)
                    matrix = []

                    for row in data[1:]:
                        if not row:  # Skip empty rows
                            continue
                        # Convert weights to numbers (skip first column which contains node names)
                        matrix_row = []
                        for x in row[1:]:
                            try:
                                matrix_row.append(float(x) if x else 0)
                            except ValueError:
                                matrix_row.append(0)  # Default to 0 if conversion fails
                        matrix.append(matrix_row)

                    self.controller.set_graph_data(nodes, matrix)
                else:
                    # Assume it's a pure numerical matrix (original behavior)
                    if len(data) > 1 and len(data[0]) == len(data):
                        nodes = [f"Node {i+1}" for i in range(len(data[0]))]
                        matrix = []
                        for row in data[1:]:
                            matrix.append([float(x) if x else 0 for x in row])
                        self.controller.set_graph_data(nodes, matrix)
                    else:
                        messagebox.showerror(
                            "Erreur",
                            "Format CSV invalide. Doit être une matrice carrée avec les noms des nœuds en première ligne et colonne, ou une matrice purement numérique",
                        )
            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Erreur lors de la lecture du fichier: {str(e)}"
                )

    def manual_input(self):
        """Handle manual input by calling the parent frame's method"""
        if hasattr(self.controller, "saisie_manuelle"):
            self.controller.saisie_manuelle()
        else:
            # If the controller doesn't have the method, call it directly on the parent frame
            parent = (
                self.controller
                if hasattr(self.controller, "saisie_manuelle")
                else self.frame.master
            )
            parent.saisie_manuelle()


class InputDijkstraPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sommets = []
        self.matrice = []
        self.edges = []  # Pour la saisie manuelle
        self.result = None  # Pour stocker le résultat
        self.start_node = tk.StringVar()
        self.end_node = tk.StringVar()

        # Apply modern styling
        self.style_widgets()
        self.create_widgets()

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
        # Clear the main frame if it exists
        if hasattr(self, "main_frame"):
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        else:
            self.main_frame = ttk.Frame(self)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel for input controls
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20))

        # Right panel for results
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Title
        title_frame = ttk.Frame(self.left_panel)
        title_frame.pack(fill="x", pady=(0, 15))
        title_label = ttk.Label(
            title_frame,
            text="Algorithme de Dijkstra",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()
        subtitle_label = ttk.Label(
            title_frame,
            text="Trouve le plus court chemin entre deux sommets",
            font=("Arial", 10),
            foreground="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 10))

        # Controls frame
        self.controls_frame = ttk.Frame(self.left_panel)
        self.controls_frame.pack(fill="x", pady=5)

        # Intégration de l'importer
        try:
            self.importer = DijkstraImporter(self.controls_frame, self)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation: {str(e)}")

        # Node selection
        node_frame = ttk.Frame(self.left_panel)
        node_frame.pack(fill="x", pady=10)

        ttk.Label(node_frame, text="Sommet de départ:").pack(anchor="w")
        self.start_combo = ttk.Combobox(node_frame, textvariable=self.start_node)
        self.start_combo.pack(fill="x", pady=(0, 5))

        ttk.Label(node_frame, text="Sommet d'arrivée:").pack(anchor="w")
        self.end_combo = ttk.Combobox(node_frame, textvariable=self.end_node)
        self.end_combo.pack(fill="x", pady=(0, 5))

        # Info frame
        info_frame = ttk.LabelFrame(self.left_panel, text="Instructions")
        info_frame.pack(fill="x", pady=10)

        info_text = (
            "• Import JSON : Importez un graphe depuis un fichier JSON\n"
            "• Import CSV : Importez un graphe depuis un fichier CSV\n"
            "• Saisie manuelle : Entrez les données du graphe manuellement\n\n"
            "Format attendu :\n"
            "- Sommets : Liste de noms (ex: A, B, C, D)\n"
            "- Matrice : Matrice d'adjacence avec les poids"
        )
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)

        # Navigation buttons
        nav_frame = ttk.Frame(self.left_panel)
        nav_frame.pack(fill="x", pady=(20, 0))

        ttk.Button(
            nav_frame,
            text="Retour au menu",
            command=lambda: self.controller.change_frame("menu"),
        ).pack(side="left", padx=5, fill="x", expand=True)

        self.run_button = ttk.Button(
            nav_frame,
            text="Lancer l'algorithme",
            command=self.run_algorithm,
            style="Accent.TButton",
        )
        self.run_button.pack(side="right", padx=5, fill="x", expand=True)

        # Status message
        self.help_label = ttk.Label(
            self.left_panel,
            text="Veuillez importer ou saisir les données du graphe avant de lancer l'algorithme",
            font=("Arial", 9, "italic"),
            foreground="#7f8c8d",
        )
        self.help_label.pack(pady=5)

        # Initialize results panel
        self.init_results_panel()

    def init_results_panel(self):
        """Initialize the results panel"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        # Title for results panel
        self.results_title = ttk.Label(
            self.right_panel,
            text="Résultats de l'algorithme",
            font=("Arial", 14, "bold"),
            foreground="#2c3e50",
        )
        self.results_title.pack(pady=(0, 10))

        # Graph info frame
        self.graph_info_frame = ttk.LabelFrame(
            self.right_panel, text="Informations du graphe"
        )
        self.graph_info_frame.pack(fill="x", pady=5, padx=5)

        # Results frame
        self.results_frame = ttk.LabelFrame(self.right_panel, text="Résultats")
        self.results_frame.pack(fill="both", expand=True, pady=5, padx=5)

        # Default message when no results
        self.default_results_label = ttk.Label(
            self.results_frame,
            text="Aucun résultat à afficher. Lancez l'algorithme pour voir les résultats.",
            font=("Arial", 10, "italic"),
            foreground="#7f8c8d",
        )
        self.default_results_label.pack(pady=50)

        # Action buttons (hidden by default)
        self.action_buttons_frame = ttk.Frame(self.right_panel)

        ttk.Button(
            self.action_buttons_frame,
            text="Retour au menu",
            command=lambda: self.controller.change_frame("menu"),
        ).pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(
            self.action_buttons_frame,
            text="Lancer à nouveau",
            command=self.run_algorithm,
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def set_graph_data(self, sommets, matrice):
        """Méthode appelée par l'importer pour définir les données du graphe"""
        self.sommets = sommets
        self.matrice = matrice

        # Update comboboxes
        self.start_combo["values"] = sommets
        self.end_combo["values"] = sommets
        if len(sommets) >= 2:
            self.start_node.set(sommets[0])
            self.end_node.set(sommets[1])

        # Update graph info in results panel
        graph_info = (
            f"- Nombre de nœuds: {len(sommets)}\n"
            f"- Nombre d'arêtes: {sum(1 for row in matrice for x in row if x != 0)}\n"
            f"- Sommets: {', '.join(sommets)}"
        )

        self.update_results_panel(
            graph_info=graph_info,
            result_text="Données du graphe chargées. Prêt à exécuter l'algorithme.",
        )

        messagebox.showinfo(
            "Données chargées",
            f"Graphe chargé avec succès!\n"
            f"Nombre de sommets : {len(sommets)}\n"
            f"Sommets : {', '.join(sommets)}",
        )

    def run_algorithm(self):
        """Lance l'algorithme avec les données importées"""
        if not self.sommets or not self.matrice:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord importer ou saisir les données du graphe"
            )
            return

        start = self.start_node.get()
        end = self.end_node.get()

        if not start or not end:
            messagebox.showwarning(
                "Attention", "Veuillez sélectionner les nœuds de départ et d'arrivée"
            )
            return

        if start not in self.sommets or end not in self.sommets:
            messagebox.showwarning(
                "Attention", "Les nœuds sélectionnés ne font pas partie du graphe"
            )
            return

        # Run Dijkstra's algorithm
        path, distance = self.dijkstra_algorithm(start, end)

        if not path:
            self.update_results_panel(
                graph_info=(
                    f"- Nombre de nœuds: {len(self.sommets)}\n"
                    f"- Nombre d'arêtes: {sum(1 for row in self.matrice for x in row if x != 0)}\n"
                    f"- Source: {start}\n"
                    f"- Destination: {end}"
                ),
                result_text=f"Aucun chemin trouvé entre {start} et {end}",
                path=None,
            )
            return

        # Update results
        graph_info = (
            f"- Nombre de nœuds: {len(self.sommets)}\n"
            f"- Nombre d'arêtes: {sum(1 for row in self.matrice for x in row if x != 0)}\n"
            f"- Source: {start}\n"
            f"- Destination: {end}"
        )

        result_text = (
            f"Plus court chemin trouvé:\n\n"
            f"De {start} à {end}:\n"
            f"Chemin: {' → '.join(path)}\n"
            f"Distance totale: {distance}\n\n"
            f"Analyse complétée avec succès."
        )

        self.update_results_panel(graph_info, result_text, path)

    def dijkstra_algorithm(self, start, end):
        """Implémentation de l'algorithme de Dijkstra"""
        # Create a mapping from node names to indices
        node_index = {node: idx for idx, node in enumerate(self.sommets)}

        # Initialize distances
        distances = {node: float("inf") for node in self.sommets}
        distances[start] = 0

        # Priority queue (using a simple list for simplicity)
        queue = [(0, start)]

        # To keep track of previous nodes in optimal path
        previous = {node: None for node in self.sommets}

        while queue:
            # Get node with smallest distance
            current_dist, current_node = min(queue)
            queue.remove((current_dist, current_node))

            # Stop if we've reached the end node
            if current_node == end:
                break

            # Get all neighbors
            current_idx = node_index[current_node]
            for neighbor_idx, weight in enumerate(self.matrice[current_idx]):
                if weight > 0:  # There's an edge
                    neighbor = self.sommets[neighbor_idx]
                    new_dist = current_dist + weight

                    # If found shorter path
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous[neighbor] = current_node
                        queue.append((new_dist, neighbor))

        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        # Return path and total distance if path exists
        if path[0] == start:
            return path, distances[end]
        else:
            return None, None

    def update_results_panel(self, graph_info, result_text, path=None):
        """Update the results panel with Dijkstra-specific visualization"""
        # Clear previous content
        for widget in self.graph_info_frame.winfo_children():
            widget.destroy()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Update graph info
        info_label = ttk.Label(
            self.graph_info_frame,
            text=graph_info,
            justify="left",
        )
        info_label.pack(padx=2, pady=2, anchor="w")

        # Create visualization frame
        viz_frame = ttk.Frame(self.results_frame)
        viz_frame.pack(fill="both", expand=True, pady=10)

        # Create figure with modern styling
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Create networkx graph
        G = nx.DiGraph()
        G.add_nodes_from(self.sommets)

        # Add edges
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets)):
                if self.matrice[i][j] > 0:
                    G.add_edge(
                        self.sommets[i], self.sommets[j], weight=self.matrice[i][j]
                    )

        # Node positioning
        pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42)

        # Draw all edges (gray)
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edge_color="#adb5bd",
            width=1.5,  # Make edges thicker
            arrows=True,  # Ensure arrows are shown
            arrowsize=20,  # Larger arrow heads
            arrowstyle="-|>",  # More pronounced arrow style
            min_source_margin=15,  # Space between node and arrow start
            min_target_margin=15,  # Space between node and arrow tip
            alpha=0.8,
        )

        # Draw edge labels (weights)
        edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            ax=ax,
            font_size=9,
            font_color="#495057",
        )

        # Highlight the shortest path if exists
        if path:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=path_edges,
                ax=ax,
                edge_color="#4a6baf",
                width=3,
                arrows=True,
                arrowsize=25,
                arrowstyle='-|>',
                min_source_margin=15,
                min_target_margin=15,
            )

        # Draw nodes with different colors for path vs non-path
        node_colors = []
        for node in G.nodes():
            if path and node in path:
                node_colors.append("#4a6baf")  # Blue for path nodes
            else:
                node_colors.append("#2c3e50")  # Dark gray for other nodes

        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            node_size=1500,
            node_color=node_colors,
            alpha=0.9,
            linewidths=0,
        )

        # Draw node labels
        nx.draw_networkx_labels(
            G,
            pos,
            ax=ax,
            font_size=11,
            font_weight="bold",
            font_color="white",
        )

        # Title with better styling
        if path:
            ax.set_title(
                f"Plus court chemin: {' → '.join(path)}",
                fontsize=11,
                fontweight="bold",
                pad=16,
            )
        else:
            ax.set_title(
                "Graphe d'entrée",
                fontsize=11,
                fontweight="bold",
                pad=16,
            )

        # Remove axes
        ax.axis("off")

        plt.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add information panel below the graph
        info_frame = ttk.Frame(self.results_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        # Result text display
        ttk.Label(
            info_frame,
            text=result_text,
            font=("Arial", 11),
            foreground="#343a40",
            justify="left",
        ).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Add details table if path exists
        if path:
            details_frame = ttk.Frame(self.results_frame)
            details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

            # Create a treeview widget
            columns = ("Étape", "Sommet", "Distance depuis le départ")
            tree = ttk.Treeview(
                details_frame, columns=columns, show="headings", height=6
            )

            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor="center")

            # Calculate distances for each node in path
            distances = self.calculate_path_distances(path)

            # Add data to table
            for i, node in enumerate(path):
                tree.insert("", "end", values=(i + 1, node, distances[node]))

            # Add scrollbar
            scrollbar = ttk.Scrollbar(
                details_frame, orient="vertical", command=tree.yview
            )
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(fill=tk.BOTH, expand=True)

        # Show action buttons
        self.action_buttons_frame.pack(fill="x", pady=(10, 0))

    def calculate_path_distances(self, path):
        """Calculate distances for each node in the path"""
        distances = {}
        total_distance = 0
        distances[path[0]] = 0

        for i in range(1, len(path)):
            from_node = path[i - 1]
            to_node = path[i]
            from_idx = self.sommets.index(from_node)
            to_idx = self.sommets.index(to_node)
            total_distance += self.matrice[from_idx][to_idx]
            distances[to_node] = total_distance

        return distances

    def clear(self):
        """Nettoie l'interface"""
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(self.master, self.controller)

    def saisie_manuelle(self):
        """Affiche l'interface de saisie manuelle"""
        # Clear only the content we need to replace
        if hasattr(self, "main_frame"):
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        else:
            self.main_frame = ttk.Frame(self)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Reset edges list
        self.edges = []

        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Saisie des arêtes")
        input_frame.pack(fill="x", padx=10, pady=10)

        # Entry fields
        ttk.Label(input_frame, text="Sommet de départ:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.from_entry = ttk.Entry(input_frame)
        self.from_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Sommet d'arrivée:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.to_entry = ttk.Entry(input_frame)
        self.to_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Poids:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Add button
        ttk.Button(
            input_frame,
            text="Ajouter l'arête",
            command=self.add_edge,
            style="Accent.TButton",
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # List of edges
        list_frame = ttk.LabelFrame(self.main_frame, text="Arêtes ajoutées")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.edges_listbox = tk.Listbox(
            list_frame, bg="white", relief="solid", borderwidth=1, font=("Arial", 10)
        )
        self.edges_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Navigation buttons
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill="x", pady=10)

        ttk.Button(nav_frame, text="Annuler", command=self.create_widgets).pack(
            side="left", padx=5, fill="x", expand=True
        )

        ttk.Button(
            nav_frame,
            text="Valider",
            command=self.validate_manual_input,
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def add_edge(self):
        """Ajoute une arête à la liste"""
        try:
            f = self.from_entry.get().strip()
            t = self.to_entry.get().strip()
            w = float(self.weight_entry.get())

            if not f or not t:
                raise ValueError("Les sommets ne peuvent pas être vides")

            self.edges.append((f, t, w))
            self.edges_listbox.insert(tk.END, f"{f} -> {t} : {w}")

            # Clear fields
            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror(
                "Erreur", str(e) if str(e) else "Le poids doit être un nombre"
            )

    def validate_manual_input(self):
        """Valide la saisie manuelle et lance l'algorithme"""
        if not self.edges:
            messagebox.showwarning("Attention", "Veuillez ajouter au moins une arête")
            return

        # Extract all unique nodes
        nodes = set()
        for f, t, _ in self.edges:
            nodes.add(f)
            nodes.add(t)

        self.sommets = sorted(nodes)

        # Create adjacency matrix
        node_index = {node: idx for idx, node in enumerate(self.sommets)}
        self.matrice = [[0] * len(self.sommets) for _ in range(len(self.sommets))]

        for f, t, w in self.edges:
            i = node_index[f]
            j = node_index[t]
            self.matrice[i][j] = w

        # Recreate the main interface
        self.create_widgets()

        # Update comboboxes
        self.start_combo["values"] = self.sommets
        self.end_combo["values"] = self.sommets
        if len(self.sommets) >= 2:
            self.start_node.set(self.sommets[0])
            self.end_node.set(self.sommets[1])

        # Update graph info
        graph_info = (
            f"- Nombre de nœuds: {len(self.sommets)}\n"
            f"- Nombre d'arêtes: {len(self.edges)}\n"
            f"- Sommets: {', '.join(self.sommets)}"
        )

        self.update_results_panel(
            graph_info=graph_info,
            result_text="Données du graphe saisies. Prêt à exécuter l'algorithme.",
        )

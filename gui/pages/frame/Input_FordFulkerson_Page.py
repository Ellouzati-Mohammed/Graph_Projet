import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from Visualisation.graph.FordFulkersonPage import FordFulkersonPage


class InputFordFulkersonPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.graph_data = {"nodes": [], "edges": [], "source": "", "sink": ""}
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
            text="Algorithme de Ford-Fulkerson",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()
        subtitle_label = ttk.Label(
            title_frame,
            text="Calcul du flot maximum dans un réseau",
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
            "   - Des arêtes avec capacités (noeud1,noeud2,capacité)\n"
            "   - Une source et un puits\n\n"
            "3. Lancez l'algorithme pour calculer\n"
            "   le flot maximum dans le réseau"
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
        self.viz_frame = ttk.LabelFrame(right_panel, text="Visualisation du réseau")
        self.viz_frame.pack(fill="both", expand=True)

        # Placeholder for graph visualization
        placeholder = ttk.Label(
            self.viz_frame,
            text="Le réseau s'affichera ici après exécution de l'algorithme",
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
                f"• Source: {self.graph_data['source']}\n"
                f"• Puits: {self.graph_data['sink']}"
            )

        self.graph_info_label.config(text=info_text)

    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                required = ["nodes", "edges", "source", "sink"]
                if not all(k in data for k in required):
                    raise ValueError("Format JSON invalide")

                # Validate and convert data
                data["edges"] = [[u, v, int(c)] for u, v, c in data["edges"]]
                data["source"] = str(data["source"])
                data["sink"] = str(data["sink"])

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
                    "source": str(data[1][0]),
                    "sink": str(data[1][1]),
                    "edges": [
                        [row[0], row[1], int(row[2])]
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
        dialog.title("Saisie manuelle du réseau")
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

        # Source and Sink
        source_sink_frame = ttk.Frame(main_frame)
        source_sink_frame.pack(fill="x", pady=5)

        ttk.Label(source_sink_frame, text="Source:").pack(side="left", padx=5)
        source_entry = ttk.Entry(source_sink_frame, width=20)
        source_entry.pack(side="left", padx=5)

        ttk.Label(source_sink_frame, text="Puits:").pack(side="left", padx=5)
        sink_entry = ttk.Entry(source_sink_frame, width=20)
        sink_entry.pack(side="left", padx=5)

        # Edges input
        edges_frame = ttk.LabelFrame(
            main_frame, text="Arêtes (une par ligne, format: noeud1,noeud2,capacité)"
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
                source_entry.get(),
                sink_entry.get(),
                edges_text.get("1.0", "end-1c"),
            ),
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def validate_manual_input(self, dialog, nodes_str, source, sink, edges_str):
        """Validate manual input data"""
        try:
            nodes = [n.strip() for n in nodes_str.split(",") if n.strip()]
            if not nodes:
                raise ValueError("Veuillez saisir au moins un noeud")

            if not source or not sink:
                raise ValueError("La source et le puits doivent être spécifiés")

            if source not in nodes:
                raise ValueError("La source doit être dans la liste des noeuds")

            if sink not in nodes:
                raise ValueError("Le puits doit être dans la liste des noeuds")

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
                        capacity = int(parts[2])
                        if capacity <= 0:
                            raise ValueError(f"Capacité doit être positive pour {line}")
                        edges.append([parts[0], parts[1], capacity])
                    except ValueError:
                        raise ValueError(
                            f"Capacité doit être un nombre entier pour {line}"
                        )

            self.graph_data = {
                "nodes": nodes,
                "edges": edges,
                "source": source,
                "sink": sink,
            }

            self.validate_data()
            self.update_graph_info()
            self.run_button.config(state="normal")
            dialog.destroy()
            messagebox.showinfo(
                "Succès", f"Réseau créé avec {len(nodes)} noeuds et {len(edges)} arêtes"
            )
            self.update_status(
                f"Réseau manuel créé: {len(nodes)} noeuds, {len(edges)} arêtes"
            )

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=dialog)
            self.update_status("Erreur dans la saisie manuelle")

    def validate_data(self):
        """Validate graph data"""
        if not self.graph_data["nodes"]:
            raise ValueError("Aucun noeud spécifié")

        if self.graph_data["source"] not in self.graph_data["nodes"]:
            raise ValueError("Source non trouvée dans les noeuds")

        if self.graph_data["sink"] not in self.graph_data["nodes"]:
            raise ValueError("Puits non trouvé dans les noeuds")

        for edge in self.graph_data["edges"]:
            if (
                edge[0] not in self.graph_data["nodes"]
                or edge[1] not in self.graph_data["nodes"]
            ):
                raise ValueError(f"Arête {edge} référence un noeud inexistant")
            if edge[2] <= 0:
                raise ValueError(f"Capacité doit être positive pour l'arête {edge}")

    def reset_data(self):
        """Reset all graph data"""
        self.graph_data = {"nodes": [], "edges": [], "source": "", "sink": ""}

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
            text="Le réseau s'affichera ici après exécution de l'algorithme",
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
        """Run Ford-Fulkerson algorithm and visualize the result using FordFulkersonPage"""
        if not self.graph_data["nodes"] or not self.graph_data["edges"]:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord importer ou saisir les données du graphe"
            )
            return

        try:
            self.update_status("Exécution de l'algorithme de Ford-Fulkerson...")

            # Supprimer le placeholder
            if hasattr(self, 'placeholder'):
                self.placeholder.pack_forget()

            # Create capacity matrix
            nodes = self.graph_data["nodes"]
            n = len(nodes)
            matrice_adjacence = [[0] * n for _ in range(n)]

            # Fill capacity matrix from edges
            for u, v, c in self.graph_data["edges"]:
                i = nodes.index(u)
                j = nodes.index(v)
                matrice_adjacence[i][j] = c

            # Prepare data for FordFulkersonPage
            data = {
                'sommets': nodes,
                'matrice': matrice_adjacence,
                'source': self.graph_data["source"],
                'sink': self.graph_data["sink"]
            }

            # Display the results using FordFulkersonPage
            self.display_ford_fulkerson_results(data)

            #self.update_status(f"Algorithme terminé - Flot maximum: {max_flow}")

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e))
            self.update_status("Erreur dans les données d'entrée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def display_ford_fulkerson_results(self, data):
        """Affiche les résultats avec la classe FordFulkersonPage"""
        # Effacer la visualisation précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer un cadre conteneur pour FordFulkersonPage
        container = ttk.Frame(self.viz_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialiser et afficher FordFulkersonPage dans le conteneur
        ford_fulkerson_page = FordFulkersonPage(container, data)
        ford_fulkerson_page.pack(fill="both", expand=True)

    def visualize_network(self, nodes, capacity_matrix, flow_matrix, max_flow):
        """Visualize the network with capacities and flows"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create directed graph
        G = nx.DiGraph()
        G.add_nodes_from(nodes)

        # Add edges with capacities and flows
        edge_labels = {}
        edge_colors = []

        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if capacity_matrix[i][j] > 0:
                    G.add_edge(nodes[i], nodes[j])
                    flow = flow_matrix[i][j]
                    capacity = capacity_matrix[i][j]

                    # Format edge label
                    edge_labels[(nodes[i], nodes[j])] = f"{flow}/{capacity}"

                    # Color coding
                    if flow == 0:
                        edge_colors.append("#cccccc")  # Gray - no flow
                    elif flow == capacity:
                        edge_colors.append("#ff6b6b")  # Red - saturated
                    else:
                        edge_colors.append("#51cf66")  # Green - flowing

        # Create figure with better layout
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Improved node positioning
        pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

        # Draw nodes with better styling
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

        # Draw labels with better styling
        nx.draw_networkx_labels(
            G, pos, ax=ax, font_size=12, font_weight="bold", font_color="white"
        )

        # Draw edges with arrows and custom styling
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

        # Edge labels with better styling
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
        ax.set_title(
            f"Réseau de flot - Flot maximum: {max_flow}",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )

        # Remove axes
        ax.axis("off")

        plt.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add information panel below the graph
        info_frame = ttk.Frame(self.viz_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        # Max flow display
        ttk.Label(
            info_frame,
            text=f"Flot maximum: {max_flow}",
            font=("Arial", 12, "bold"),
            foreground="#2b8a3e",
        ).pack(side=tk.LEFT, padx=10)

        # Legend
        legend_frame = ttk.Frame(info_frame)
        legend_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(legend_frame, text="Légende:").pack(anchor="w")
        ttk.Label(legend_frame, text="• Gris: Pas de flot", foreground="#868e96").pack(
            anchor="w"
        )
        ttk.Label(legend_frame, text="• Vert: Flot partiel", foreground="#51cf66").pack(
            anchor="w"
        )
        ttk.Label(
            legend_frame, text="• Rouge: Flot maximal", foreground="#ff6b6b"
        ).pack(anchor="w")

        # Add flow details table
        details_frame = ttk.Frame(self.viz_frame)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Create a treeview widget
        columns = ("Source", "Destination", "Flot", "Capacité", "Saturation")
        tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=6)

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Add data
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if capacity_matrix[i][j] > 0:
                    flow = flow_matrix[i][j]
                    cap = capacity_matrix[i][j]
                    saturation = f"{(flow/cap)*100:.1f}%" if cap > 0 else "0%"

                    tree.insert(
                        "", "end", values=(nodes[i], nodes[j], flow, cap, saturation)
                    )

        # Add scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)


def fordFulkerson(nodes, capacity_matrix, source, sink):
    """Implementation of Ford-Fulkerson algorithm using BFS (Edmonds-Karp)"""
    n = len(nodes)
    source_idx = nodes.index(source)
    sink_idx = nodes.index(sink)

    # Initialize flow matrix
    flow_matrix = [[0] * n for _ in range(n)]
    residual_graph = [[0] * n for _ in range(n)]

    # Create residual graph
    for i in range(n):
        for j in range(n):
            residual_graph[i][j] = capacity_matrix[i][j]

    parent = [-1] * n
    max_flow = 0

    def bfs(residual_graph, s, t, parent):
        visited = [False] * n
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v in range(n):
                if not visited[v] and residual_graph[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == t:
                        return True
        return False

    # Find augmenting paths and update flows
    while bfs(residual_graph, source_idx, sink_idx, parent):
        path_flow = float("Inf")
        s = sink_idx

        # Find minimum residual capacity along the path
        while s != source_idx:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Update residual capacities and flow matrix
        v = sink_idx
        while v != source_idx:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            flow_matrix[u][v] += path_flow
            v = u

        max_flow += path_flow

    return max_flow, flow_matrix

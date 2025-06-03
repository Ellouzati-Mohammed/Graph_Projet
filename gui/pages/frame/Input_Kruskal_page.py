import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx


class InputKruskal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sommets = []
        self.matrice = []
        self.edges = []
        self.canvas_widget = None

        self.create_widgets()
        self.style_widgets()

    def style_widgets(self):
        """Apply modern styling to widgets"""
        style = ttk.Style()
        style.theme_use("clam")  # Use a modern theme

        # Configure styles
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=6)
        style.configure(
            "Accent.TButton",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#4a6baf",
        )
        style.configure(
            "TLabelframe",
            background="#f0f0f0",
            relief="groove",
            borderwidth=2,
            labelmargins=(0, 0, 10, 5),
        )
        style.configure(
            "TLabelframe.Label",
            background="#f0f0f0",
            font=("Arial", 10, "bold"),
            foreground="#2c3e50",
        )
        style.configure("TEntry", padding=5)
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", "#4a6baf")])
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
            text="Algorithme de Kruskal",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()
        subtitle_label = ttk.Label(
            title_frame,
            text="Arbre couvrant de poids minimal",
            font=("Arial", 10),
            foreground="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 10))

        # Graph info display
        self.graph_info_frame = ttk.LabelFrame(
            left_panel, text="Informations du graphe", style="TLabelframe"
        )
        self.graph_info_frame.pack(fill="x", pady=5)
        self.graph_info_label = ttk.Label(
            self.graph_info_frame, text="Aucun graphe chargé", justify="left"
        )
        self.graph_info_label.pack(padx=5, pady=5)

        # Import section
        import_frame = ttk.LabelFrame(
            left_panel, text="Importation des données", style="TLabelframe"
        )
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
        info_frame = ttk.LabelFrame(
            left_panel, text="Instructions", style="TLabelframe"
        )
        info_frame.pack(fill="x", pady=5)
        info_text = (
            "1. Importez un graphe depuis un fichier (JSON/CSV)\n"
            "   ou saisissez les données manuellement\n\n"
            "2. Format attendu :\n"
            "   - Sommets : Liste de noms (ex: A, B, C, D)\n"
            "   - Matrice : Matrice d'adjacence pondérée\n"
            "   - Arêtes : Liste de triplets (ex: A-B-3)\n\n"
            "3. Lancez l'algorithme pour trouver\n"
            "   l'arbre couvrant minimal"
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
        self.viz_frame = ttk.LabelFrame(
            right_panel, text="Visualisation du graphe", style="TLabelframe"
        )
        self.viz_frame.pack(fill="both", expand=True)

        # Placeholder for graph visualization
        self.placeholder = ttk.Label(
            self.viz_frame,
            text="Le graphe s'affichera ici après exécution de l'algorithme",
            justify="center",
            font=("Arial", 10, "italic"),
            foreground="#7f8c8d",
        )
        self.placeholder.pack(expand=True, fill="both")

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
        if not self.sommets:
            info_text = "Aucun graphe chargé"
        else:
            total_weight = (
                sum(edge[2] for edge in self.edges) / 2
            )  # Divisé par 2 car chaque arête est comptée deux fois
            info_text = (
                f"• Nombre de sommets: {len(self.sommets)}\n"
                f"• Nombre d'arêtes: {len(self.edges)}\n"
                f"• Poids total: {total_weight:.2f}"
            )

        self.graph_info_label.config(text=info_text)

    def import_json(self):
        """Importe un graphe depuis un fichier JSON"""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                if "sommets" not in data or "matrice" not in data:
                    raise ValueError(
                        "Format JSON invalide. Doit contenir 'sommets' et 'matrice'"
                    )

                self.sommets = data["sommets"]
                self.matrice = data["matrice"]
                self.edges = []

                # Convertit la matrice en liste d'arêtes
                for i in range(len(self.sommets)):
                    for j in range(len(self.sommets)):
                        poids = self.matrice[i][j]
                        if poids > 0 and i < j:  # Évite les doublons
                            self.edges.append((self.sommets[i], self.sommets[j], poids))

                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès", f"Graphe importé avec {len(self.sommets)} sommets"
                )
                self.update_status(f"Graphe JSON chargé: {len(self.sommets)} sommets")

            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Erreur lors de l'import JSON: {str(e)}"
                )
                self.update_status("Erreur lors de l'importation JSON")

    def import_csv(self):
        """Importe un graphe depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                edges = []
                sommets = set()

                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 3:
                            f, t, w = row[0], row[1], float(row[2])
                            edges.append((f, t, w))
                            sommets.add(f)
                            sommets.add(t)

                self.sommets = list(sommets)
                self.edges = edges

                # Crée la matrice d'adjacence
                n = len(self.sommets)
                self.matrice = [[0] * n for _ in range(n)]

                for f, t, w in edges:
                    i = self.sommets.index(f)
                    j = self.sommets.index(t)
                    self.matrice[i][j] = w
                    self.matrice[j][i] = w

                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès",
                    f"Graphe importé avec {len(self.sommets)} sommets et {len(edges)} arêtes",
                )
                self.update_status(
                    f"Graphe CSV chargé: {len(self.sommets)} sommets, {len(edges)} arêtes"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import CSV: {str(e)}")
                self.update_status("Erreur lors de l'importation CSV")

    def show_manual_input(self):
        """Affiche la boîte de dialogue pour la saisie manuelle"""
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
            main_frame, text="Sommets (séparés par des virgules)", style="TLabelframe"
        )
        nodes_frame.pack(fill="x", pady=5)
        nodes_entry = ttk.Entry(nodes_frame)
        nodes_entry.pack(fill="x", padx=5, pady=5)

        # Edges input
        edges_frame = ttk.LabelFrame(
            main_frame,
            text="Arêtes (une par ligne, format: sommet1,sommet2,poids)",
            style="TLabelframe",
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
                edges_text.get("1.0", "end-1c"),
            ),
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def validate_manual_input(self, dialog, nodes_str, edges_str):
        """Validate manual input data"""
        try:
            nodes = [n.strip() for n in nodes_str.split(",") if n.strip()]
            if not nodes:
                raise ValueError("Veuillez saisir au moins un sommet")

            edges = []
            for line in edges_str.split("\n"):
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        raise ValueError(f"Format d'arête invalide: {line}")
                    if parts[0] not in nodes or parts[1] not in nodes:
                        raise ValueError(f"Arête {line} référence un sommet inexistant")
                    try:
                        weight = float(parts[2])
                        if weight <= 0:
                            raise ValueError(f"Poids doit être positif pour {line}")
                        edges.append((parts[0], parts[1], weight))
                    except ValueError:
                        raise ValueError(f"Poids doit être un nombre pour {line}")

            # Check for duplicate edges
            seen = set()
            for v1, v2, w in edges:
                edge = (min(v1, v2), max(v1, v2))
                if edge in seen:
                    raise ValueError(f"Arête {v1}-{v2} est en double")
                seen.add(edge)

            self.sommets = nodes
            self.edges = edges

            # Crée la matrice d'adjacence
            n = len(self.sommets)
            self.matrice = [[0] * n for _ in range(n)]

            for v1, v2, w in self.edges:
                i = self.sommets.index(v1)
                j = self.sommets.index(v2)
                self.matrice[i][j] = w
                self.matrice[j][i] = w

            self.update_graph_info()
            self.run_button.config(state="normal")
            dialog.destroy()
            messagebox.showinfo(
                "Succès",
                f"Graphe créé avec {len(nodes)} sommets et {len(edges)} arêtes",
            )
            self.update_status(
                f"Graphe manuel créé: {len(nodes)} sommets, {len(edges)} arêtes"
            )

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=dialog)
            self.update_status("Erreur dans la saisie manuelle")

    def reset_data(self):
        """Reset all graph data"""
        self.sommets = []
        self.matrice = []
        self.edges = []

        # Update graph info display
        self.update_graph_info()

        # Disable run button
        self.run_button.config(state="disabled")

        # Clear visualization
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None

        # Add placeholder back
        self.placeholder.pack(expand=True, fill="both")

        messagebox.showinfo(
            "Réinitialisation", "Toutes les données ont été réinitialisées"
        )
        self.update_status("Prêt - Données réinitialisées")

    def run_algorithm(self):
        """Exécute l'algorithme de Kruskal et visualise le graphe"""
        if not self.sommets or not self.matrice:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord importer ou saisir les données du graphe"
            )
            return

        try:
            self.update_status("Exécution de l'algorithme de Kruskal...")

            # Exécute l'algorithme de Kruskal
            mst_edges = kruskal(self.sommets, self.matrice)

            # Visualize the result
            self.visualize_graph(self.sommets, self.edges, mst_edges)

            # Calculate total weight
            total_weight = sum(edge[2] for edge in mst_edges)
            self.update_status(f"Algorithme terminé - Poids total: {total_weight}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def visualize_graph(self, nodes, edges, mst_edges):
        """Visualize the graph with MST highlighted"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create undirected graph
        G = nx.Graph()
        G.add_nodes_from(nodes)

        # Add all edges
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])

        # Create figure
        fig = plt.figure(figsize=(10, 6), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        # Improved node positioning
        pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

        # Prepare edge colors and widths
        edge_colors = []
        edge_widths = []

        # Determine which edges are in MST
        mst_edge_set = set()
        for edge in mst_edges:
            mst_edge_set.add((edge[0], edge[1]))
            mst_edge_set.add((edge[1], edge[0]))  # Add both directions

        # Style edges based on whether they're in MST
        for edge in G.edges():
            if edge in mst_edge_set or (edge[1], edge[0]) in mst_edge_set:
                edge_colors.append("#ff6b6b")  # Red for MST edges
                edge_widths.append(3)
            else:
                edge_colors.append("#cccccc")  # Gray for non-MST edges
                edge_widths.append(1)

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

        # Draw edges with custom styling
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edge_color=edge_colors,
            width=edge_widths,
        )

        # Edge labels with weights
        edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
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
        total_weight = sum(edge[2] for edge in mst_edges)
        ax.set_title(
            f"Arbre couvrant minimal - Poids total: {total_weight}",
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
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add information panel below the graph
        info_frame = ttk.Frame(self.viz_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        # Total weight display
        ttk.Label(
            info_frame,
            text=f"Poids total: {total_weight}",
            font=("Arial", 12, "bold"),
            foreground="#2b8a3e",
        ).pack(side=tk.LEFT, padx=10)

        # Legend
        legend_frame = ttk.Frame(info_frame)
        legend_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(legend_frame, text="Légende:").pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Gris: Arêtes du graphe", foreground="#868e96"
        ).pack(anchor="w")
        ttk.Label(
            legend_frame, text="• Rouge: Arêtes de l'ACM", foreground="#ff6b6b"
        ).pack(anchor="w")

        # Add MST edges details table
        details_frame = ttk.Frame(self.viz_frame)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Create a treeview widget
        columns = ("Sommet 1", "Sommet 2", "Poids")
        tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=6)

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Add data
        for edge in sorted(mst_edges, key=lambda x: (x[0], x[1])):
            tree.insert("", "end", values=(edge[0], edge[1], edge[2]))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)


def kruskal(nodes, matrix):
    """Implementation of Kruskal's algorithm for MST"""
    # Create list of all edges
    edges = []
    n = len(nodes)
    for i in range(n):
        for j in range(i + 1, n):  # Only upper triangle to avoid duplicates
            if matrix[i][j] > 0:
                edges.append((nodes[i], nodes[j], matrix[i][j]))

    # Sort edges by weight
    edges.sort(key=lambda x: x[2])

    parent = {node: node for node in nodes}

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]  # Path compression
            u = parent[u]
        return u

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            parent[root_v] = root_u

    mst_edges = []

    for edge in edges:
        u, v, weight = edge
        if find(u) != find(v):
            union(u, v)
            mst_edges.append(edge)

    return mst_edges

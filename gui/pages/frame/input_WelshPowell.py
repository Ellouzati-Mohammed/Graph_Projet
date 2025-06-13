import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from algorithms.graph.Welsh_Powell import Welsh_Powell
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Visualisation.graph.WelshPowellPage import WelshPowellPage



class InputWelshPowell(tk.Frame):
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
            text="Algorithme de Welsh-Powell",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()
        subtitle_label = ttk.Label(
            title_frame,
            text="Coloration de graphes avec nombre minimal de couleurs",
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
            "   - Des sommets (noms uniques)\n"
            "   - Des arêtes entre ces sommets\n\n"
            "3. Lancez l'algorithme pour obtenir\n"
            "   la coloration optimale du graphe"
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

    def import_json(self):
        """Import graph from JSON file"""
        self.update_status("Importation du fichier JSON...")
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

                # Convert matrix to edges
                for i in range(len(self.sommets)):
                    for j in range(len(self.sommets)):
                        if self.matrice[i][j] == 1 and i < j:
                            self.edges.append((self.sommets[i], self.sommets[j]))

                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès", f"Graphe importé avec {len(self.sommets)} sommets"
                )
                self.update_status(
                    f"Graphe chargé: {len(self.sommets)} sommets, {len(self.edges)} arêtes"
                )

            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Erreur lors de l'import JSON: {str(e)}"
                )
                self.update_status("Erreur lors de l'importation")

    def import_csv(self):
        """Import graph from CSV file"""
        self.update_status("Importation du fichier CSV...")
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                edges = []
                sommets = set()

                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 2:
                            f, t = row[0], row[1]
                            edges.append((f, t))
                            sommets.add(f)
                            sommets.add(t)

                self.sommets = list(sommets)
                self.edges = edges

                # Create adjacency matrix
                n = len(self.sommets)
                self.matrice = [[0] * n for _ in range(n)]

                for f, t in edges:
                    i = self.sommets.index(f)
                    j = self.sommets.index(t)
                    self.matrice[i][j] = 1
                    self.matrice[j][i] = 1

                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo(
                    "Succès",
                    f"Graphe importé avec {len(self.sommets)} sommets et {len(edges)} arêtes",
                )
                self.update_status(
                    f"Graphe chargé: {len(self.sommets)} sommets, {len(edges)} arêtes"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import CSV: {str(e)}")
                self.update_status("Erreur lors de l'importation")

    def show_manual_input(self):
        """Show manual input dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle du graphe")
        dialog.geometry("500x500")
        dialog.resizable(False, False)

        # Apply styling to dialog
        dialog.configure(bg="#f0f0f0")

        # Input Frame
        input_frame = ttk.LabelFrame(dialog, text="Ajouter une arête")
        input_frame.pack(fill="x", padx=10, pady=10)

        # Vertex 1
        ttk.Label(input_frame, text="Sommet 1:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.vertex1_entry = ttk.Entry(input_frame)
        self.vertex1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Vertex 2
        ttk.Label(input_frame, text="Sommet 2:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.vertex2_entry = ttk.Entry(input_frame)
        self.vertex2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Add button
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(
            btn_frame,
            text="Ajouter",
            command=lambda: self.add_edge(dialog),
            style="Accent.TButton",
        ).pack(side="left", padx=5)

        # List of edges
        list_frame = ttk.LabelFrame(dialog, text="Arêtes ajoutées")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar for edges list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.edges_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectbackground="#4a6baf",
            selectforeground="white",
            font=("Arial", 10),
        )
        self.edges_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.edges_listbox.yview)

        # Navigation buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(
            side="left", padx=5, fill="x", expand=True
        )
        ttk.Button(
            button_frame,
            text="Valider",
            command=lambda: self.validate_manual_input(dialog),
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

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

    def add_edge(self, dialog):
        """Add an edge to the list"""
        try:
            v1 = self.vertex1_entry.get().strip()
            v2 = self.vertex2_entry.get().strip()

            if not v1 or not v2:
                raise ValueError("Les noms des sommets ne peuvent pas être vides")

            if v1 == v2:
                raise ValueError("Une arête ne peut pas relier un sommet à lui-même")

            # Check for duplicate edges
            if (v1, v2) in self.edges or (v2, v1) in self.edges:
                raise ValueError(f"L'arête entre {v1} et {v2} existe déjà")

            self.edges.append((v1, v2))
            self.edges_listbox.insert(tk.END, f"{v1} — {v2}")

            # Clear fields
            self.vertex1_entry.delete(0, tk.END)
            self.vertex2_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=dialog)

    def validate_manual_input(self, dialog):
        """Validate manual input and create graph data"""
        if not self.edges:
            messagebox.showwarning(
                "Attention", "Veuillez ajouter au moins une arête", parent=dialog
            )
            return

        # Get all unique vertices
        sommets = set()
        for v1, v2 in self.edges:
            sommets.add(v1)
            sommets.add(v2)

        self.sommets = list(sommets)

        # Create adjacency matrix
        n = len(self.sommets)
        self.matrice = [[0] * n for _ in range(n)]

        for v1, v2 in self.edges:
            i = self.sommets.index(v1)
            j = self.sommets.index(v2)
            self.matrice[i][j] = 1
            self.matrice[j][i] = 1

        self.update_graph_info()
        self.run_button.config(state="normal")
        dialog.destroy()
        messagebox.showinfo(
            "Succès",
            f"Graphe créé avec {len(self.sommets)} sommets et {len(self.edges)} arêtes",
        )
        self.update_status(
            f"Graphe manuel créé: {len(self.sommets)} sommets, {len(self.edges)} arêtes"
        )

    def update_graph_info(self):
        """Update the graph information display"""
        if not self.sommets:
            info_text = "Aucun graphe chargé"
        else:
            info_text = (
                f"• Nombre de sommets: {len(self.sommets)}\n"
                f"• Nombre d'arêtes: {len(self.edges)}\n"
                f"• Degré maximal: {self.calculate_max_degree()}"
            )

        self.graph_info_label.config(text=info_text)

    def calculate_max_degree(self):
        """Calculate maximum degree of the graph"""
        if not self.matrice:
            return 0

        max_degree = 0
        for row in self.matrice:
            degree = sum(row)
            if degree > max_degree:
                max_degree = degree
        return max_degree

    def run_algorithm(self):
        """Exécute l'algorithme de Welsh-Powell et visualise le résultat avec WelshPowellPage"""
        if not self.sommets or not self.matrice:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord importer ou saisir les données du graphe"
            )
            return

        try:
            self.update_status("Exécution de l'algorithme de Welsh-Powell...")

            # Exécuter l'algorithme de Welsh-Powell
            colored_vertices = Welsh_Powell(self.sommets, self.matrice)
            
            # Calculer le nombre de couleurs utilisées
            num_colors = len(set(c[1] for c in colored_vertices))

            # Préparer les données pour WelshPowellPage
            data = {
                'sommets': self.sommets,
                'matrice': self.matrice,
                'colored_vertices': colored_vertices,
                'num_colors': num_colors
            }

            # Afficher les résultats avec WelshPowellPage
            self.display_welsh_powell_results(data)

            self.update_status(
                f"Algorithme terminé - {num_colors} couleurs utilisées"
            )

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def display_welsh_powell_results(self, data):
        """Affiche les résultats avec la classe WelshPowellPage"""
        # Effacer la visualisation précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer un cadre conteneur pour WelshPowellPage
        container = ttk.Frame(self.viz_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialiser et afficher WelshPowellPage dans le conteneur
        welsh_powell_page = WelshPowellPage(container, self.controller, data)
        welsh_powell_page.pack(fill="both", expand=True)

    def create_graph_visualization(self, parent_frame):
        """Crée la visualisation du graphe avec les sommets colorés"""
        sommets = self.data['sommets']
        matrice = self.data['matrice']
        colored_vertices = self.data['colored_vertices']
        
        # Créer le graphe
        G = nx.Graph()
        G.add_nodes_from(sommets)
        
        # Ajouter les arêtes
        for i in range(len(sommets)):
            for j in range(i + 1, len(sommets)):
                if matrice[i][j] > 0:
                    G.add_edge(sommets[i], sommets[j])
        
        # Créer la carte de couleurs
        color_map = []
        color_palette = plt.cm.tab10.colors  # Palette de 10 couleurs
        
        for sommet in sommets:
            index = sommets.index(sommet)
            color_code = None
            for colored in colored_vertices:
                if colored[0] == index:
                    color_code = colored[1]
                    break
            
            # Trouver la couleur RGB correspondante
            if color_code is not None:
                color_idx = color_code % len(color_palette)
                color_rgb = color_palette[color_idx]
                color_map.append(color_rgb)
            else:
                # Couleur par défaut si non trouvée
                color_map.append("#cccccc")
        
        # Créer la figure
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f0f0f0')  # Fond clair pour correspondre au thème
        
        # Positionnement des nœuds
        pos = nx.spring_layout(G, seed=42)  # Positionnement cohérent
        
        # Dessiner le graphe
        nx.draw_networkx(
            G, 
            pos, 
            ax=ax,
            node_color=color_map, 
            node_size=800,
            edge_color="gray",
            width=1.5,
            font_size=10,
            font_weight="bold",
            with_labels=True
        )
        
        # Titre
        ax.set_title("Coloration des sommets", fontsize=12, pad=15)
        
        # Désactiver les axes
        ax.set_axis_off()
        
        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Stocker une référence pour éviter la destruction par le garbage collector
        self.canvas_widget = canvas
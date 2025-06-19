import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from Visualisation.Programation_leaner.vogelsPage import VogelsApproximationPage


class InputVogelsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.supply = []
        self.demand = []
        self.costs = []
        self.canvas_widget = None

        self.style_widgets()
        self.create_widgets()

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

        # Title frame
        title_frame = ttk.Frame(left_panel)
        title_frame.pack(fill="x", pady=(0, 15))

        title_label = ttk.Label(
            title_frame,
            text="Algorithme de Vogel (VAM)",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Résolution de problème de transport",
            font=("Arial", 10),
            foreground="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 10))

        # Data info display
        self.data_info_frame = ttk.LabelFrame(
            left_panel, text="Données du problème", style="TLabelframe"
        )
        self.data_info_frame.pack(fill="x", pady=5)
        self.data_info_label = ttk.Label(
            self.data_info_frame, text="Aucune donnée chargée", justify="left"
        )
        self.data_info_label.pack(padx=5, pady=5)

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
            "1. Importez les données depuis un fichier (JSON/CSV)\n"
            "   ou saisissez les données manuellement\n\n"
            "2. Format attendu :\n"
            "   - Offres (supply) : Liste des quantités disponibles\n"
            "   - Demandes (demand) : Liste des quantités requises\n"
            "   - Coûts (costs) : Matrice des coûts de transport\n\n"
            "3. La somme des offres doit être égale à la somme des demandes"
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
            right_panel, text="Résultats de l'algorithme", style="TLabelframe"
        )
        self.viz_frame.pack(fill="both", expand=True)

        # Placeholder for results
        self.placeholder = ttk.Label(
            self.viz_frame,
            text="Les résultats s'afficheront ici après exécution de l'algorithme",
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

    def update_data_info(self):
        """Update the data information display"""
        if not self.supply or not self.demand or not self.costs:
            info_text = "Aucune donnée chargée"
        else:
            info_text = (
                f"• Sources: {len(self.supply)}\n"
                f"• Destinations: {len(self.demand)}\n"
                f"• Offres totales: {sum(self.supply)}\n"
                f"• Demandes totales: {sum(self.demand)}"
            )

        self.data_info_label.config(text=info_text)

    def reset_data(self):
        """Reset all data"""
        self.supply = []
        self.demand = []
        self.costs = []

        # Clear visualization
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None

        # Add placeholder back
        self.placeholder.pack(expand=True, fill="both")

        self.update_data_info()
        self.run_button.config(state="disabled")
        messagebox.showinfo(
            "Réinitialisation", "Toutes les données ont été réinitialisées"
        )
        self.update_status("Prêt - Données réinitialisées")

    def import_json(self):
        """Importe les données depuis un fichier JSON"""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                if not all(key in data for key in ["supply", "demand", "costs"]):
                    raise ValueError("Format JSON invalide")

                self.supply = data["supply"]
                self.demand = data["demand"]
                self.costs = data["costs"]

                self.validate_data()
                self.update_data_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.update_status(
                    f"Données JSON chargées: {len(self.supply)} sources, {len(self.demand)} destinations"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")
                self.update_status("Erreur lors de l'importation JSON")

    def import_csv(self):
        """Importe les données depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)

                if len(data) < 3:
                    raise ValueError(
                        "Le fichier CSV doit contenir au moins 3 lignes : offres, demandes et coûts"
                    )

                # Première ligne : offres
                self.supply = [float(x) for x in data[0]]

                # Deuxième ligne : demandes
                self.demand = [float(x) for x in data[1]]

                # Reste : matrice des coûts
                self.costs = [[float(x) for x in row] for row in data[2:]]

                self.validate_data()
                self.update_data_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.update_status(
                    f"Données CSV chargées: {len(self.supply)} sources, {len(self.demand)} destinations"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")
                self.update_status("Erreur lors de l'importation CSV")

    def show_manual_input(self):
        """Affiche l'interface de saisie manuelle"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle VAM")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f0f0")

        # Main container
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Supply input
        supply_frame = ttk.LabelFrame(
            main_frame,
            text="Offres (supply) - Quantités disponibles séparées par des virgules",
            style="TLabelframe",
        )
        supply_frame.pack(fill="x", pady=5)
        supply_entry = ttk.Entry(supply_frame)
        supply_entry.pack(fill="x", padx=5, pady=5)

        # Demand input
        demand_frame = ttk.LabelFrame(
            main_frame,
            text="Demandes (demand) - Quantités requises séparées par des virgules",
            style="TLabelframe",
        )
        demand_frame.pack(fill="x", pady=5)
        demand_entry = ttk.Entry(demand_frame)
        demand_entry.pack(fill="x", padx=5, pady=5)

        # Costs input
        costs_frame = ttk.LabelFrame(
            main_frame,
            text="Coûts (costs) - Une ligne par source, valeurs séparées par des virgules",
            style="TLabelframe",
        )
        costs_frame.pack(fill="both", expand=True, pady=5)
        costs_text = tk.Text(costs_frame, height=10, width=40)
        costs_text.pack(fill="both", expand=True, padx=5, pady=5)

        def validate_and_save():
            try:
                # Récupérer et valider les offres
                self.supply = [
                    float(x.strip()) for x in supply_entry.get().split(",") if x.strip()
                ]
                if not self.supply:
                    raise ValueError("Veuillez saisir au moins une offre")

                # Récupérer et valider les demandes
                self.demand = [
                    float(x.strip()) for x in demand_entry.get().split(",") if x.strip()
                ]
                if not self.demand:
                    raise ValueError("Veuillez saisir au moins une demande")

                # Récupérer et valider les coûts
                costs_lines = costs_text.get("1.0", "end-1c").strip().split("\n")
                self.costs = [
                    [float(x.strip()) for x in line.split(",") if x.strip()]
                    for line in costs_lines
                    if line.strip()
                ]
                if not self.costs:
                    raise ValueError("Veuillez saisir la matrice des coûts")

                self.validate_data()
                self.update_data_info()
                self.run_button.config(state="normal")
                dialog.destroy()
                messagebox.showinfo(
                    "Succès",
                    f"Problème créé avec {len(self.supply)} sources et {len(self.demand)} destinations",
                )
                self.update_status(
                    f"Données manuelles chargées: {len(self.supply)} sources, {len(self.demand)} destinations"
                )

            except ValueError as e:
                messagebox.showerror("Erreur de saisie", str(e), parent=dialog)
                self.update_status("Erreur dans la saisie manuelle")

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(
            side="left", padx=5, fill="x", expand=True
        )

        ttk.Button(
            button_frame,
            text="Valider",
            command=validate_and_save,
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def validate_data(self):
        """Valide les données saisies"""
        if not self.supply or not self.demand or not self.costs:
            raise ValueError("Toutes les données sont requises")

        if len(self.costs) != len(self.supply):
            raise ValueError(
                "Le nombre de lignes de la matrice des coûts doit correspondre au nombre d'offres"
            )

        if len(self.costs[0]) != len(self.demand):
            raise ValueError(
                "Le nombre de colonnes de la matrice des coûts doit correspondre au nombre de demandes"
            )

        if abs(sum(self.supply) - sum(self.demand)) > 1e-10:
            raise ValueError(
                "La somme des offres doit être égale à la somme des demandes"
            )

    def run_algorithm(self):
        """Lance l'algorithme avec les données saisies"""
        try:
            self.validate_data()
            self.update_status("Exécution de l'algorithme de Vogel...")

            # Run Vogel's algorithm
            solution, total_cost = self.vogels_algorithm()

            # Prepare data for display
            data = {
                "supply": self.supply,
                "demand": self.demand,
                "costs": self.costs,
                "solution": solution,
                "total_cost": total_cost,
            }

            # Display results
            self.display_vogels_results(data)

            self.update_status("Algorithme de Vogel exécuté avec succès")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Erreur lors du lancement de l'algorithme: {str(e)}"
            )
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def vogels_algorithm(self):
        """Implementation of Vogel's Approximation Method"""
        # Make copies of supply and demand to avoid modifying originals
        supply = self.supply.copy()
        demand = self.demand.copy()
        costs = [row.copy() for row in self.costs]

        solution = {}
        total_cost = 0

        while True:
            # Calculate penalty for each row and column
            row_penalties = []
            for i in range(len(supply)):
                if supply[i] == 0:
                    row_penalties.append(-1)
                    continue
                row = [costs[i][j] for j in range(len(demand)) if demand[j] > 0]
                if len(row) < 2:
                    row_penalties.append(0)
                else:
                    row_sorted = sorted(row)
                    row_penalties.append(row_sorted[1] - row_sorted[0])

            col_penalties = []
            for j in range(len(demand)):
                if demand[j] == 0:
                    col_penalties.append(-1)
                    continue
                col = [costs[i][j] for i in range(len(supply)) if supply[i] > 0]
                if len(col) < 2:
                    col_penalties.append(0)
                else:
                    col_sorted = sorted(col)
                    col_penalties.append(col_sorted[1] - col_sorted[0])

            # Find maximum penalty
            max_row_penalty = max(row_penalties)
            max_col_penalty = max(col_penalties)

            if max_row_penalty < 0 and max_col_penalty < 0:
                break  # All allocations done

            if max_row_penalty >= max_col_penalty:
                # Process row with max penalty
                i = row_penalties.index(max_row_penalty)
                # Find minimum cost in this row
                min_cost = float("inf")
                best_j = -1
                for j in range(len(demand)):
                    if demand[j] > 0 and costs[i][j] < min_cost:
                        min_cost = costs[i][j]
                        best_j = j
            else:
                # Process column with max penalty
                j = col_penalties.index(max_col_penalty)
                # Find minimum cost in this column
                min_cost = float("inf")
                best_i = -1
                for i in range(len(supply)):
                    if supply[i] > 0 and costs[i][j] < min_cost:
                        min_cost = costs[i][j]
                        best_i = i
                i = best_i
                best_j = j

            # Make allocation
            allocation = min(supply[i], demand[best_j])
            solution[(i, best_j)] = allocation
            total_cost += allocation * costs[i][best_j]

            # Update supply and demand
            supply[i] -= allocation
            demand[best_j] -= allocation

            # If supply or demand becomes zero, mark those costs as unavailable
            if supply[i] == 0:
                for j in range(len(demand)):
                    costs[i][j] = float("inf")
            if demand[best_j] == 0:
                for i in range(len(supply)):
                    costs[i][best_j] = float("inf")

        return solution, total_cost

    def display_vogels_results(self, data):
        """Affiche les résultats avec la classe VogelsApproximationPage (même style que MoindreCoutPage)"""
        # Effacer la visualisation précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer un cadre conteneur pour VogelsApproximationPage
        container = ttk.Frame(self.viz_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialiser et afficher VogelsApproximationPage dans le conteneur
        vogels_page = VogelsApproximationPage(container)
        vogels_page.set_data(data)
        vogels_page.pack(fill="both", expand=True)

    def create_allocation_table(self, parent, solution):
        """Create a table showing the allocation matrix in grid format"""
        # Main frame for the table
        table_frame = ttk.Frame(parent, style="White.TFrame")
        table_frame.pack()

        # Create headers for destinations
        for j in range(len(self.demand)):
            header = ttk.Label(
                table_frame,
                text=f"D{j+1}",
                font=("Arial", 9, "bold"),
                padding=(5, 2),
                relief="ridge",
                width=5,
                anchor="center",
                background="#f0f0f0",
            )
            header.grid(row=0, column=j + 1, sticky="nsew")

        # Create rows for sources and their allocations
        for i in range(len(self.supply)):
            # Source label
            source_label = ttk.Label(
                table_frame,
                text=f"S{i+1}",
                font=("Arial", 9, "bold"),
                padding=(5, 2),
                relief="ridge",
                width=5,
                anchor="center",
                background="#e6f3ff",
            )
            source_label.grid(row=i + 1, column=0, sticky="nsew")

            # Allocation values
            for j in range(len(self.demand)):
                alloc = solution.get((i, j), 0)
                alloc_label = ttk.Label(
                    table_frame,
                    text=str(alloc),
                    font=("Arial", 9),
                    padding=(5, 2),
                    relief="ridge",
                    width=5,
                    anchor="center",
                    background="white",
                )
                alloc_label.grid(row=i + 1, column=j + 1, sticky="nsew")

        # Configure grid weights
        for i in range(len(self.supply) + 1):
            table_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.demand) + 1):
            table_frame.grid_columnconfigure(j, weight=1)

    def create_allocation_matrix(self, parent, solution):
        """Create a table showing the allocation matrix"""
        matrix_frame = ttk.LabelFrame(
            parent, text="Allocation des ressources", padding=10, style="TLabelframe"
        )
        matrix_frame.pack(fill="x", pady=(0, 10))

        # Create a grid layout for the matrix
        grid_frame = ttk.Frame(matrix_frame)
        grid_frame.pack()

        # Create headers for destinations
        for j in range(len(self.demand)):
            ttk.Label(
                grid_frame,
                text=f"D{j+1}",
                font=("Arial", 9, "bold"),
                padding=5,
                relief="ridge",
                width=8,
            ).grid(row=0, column=j + 1, sticky="nsew")

        # Create rows for sources and their allocations
        for i in range(len(self.supply)):
            # Source label
            ttk.Label(
                grid_frame,
                text=f"S{i+1}",
                font=("Arial", 9, "bold"),
                padding=5,
                relief="ridge",
                width=8,
            ).grid(row=i + 1, column=0, sticky="nsew")

            # Allocation values
            for j in range(len(self.demand)):
                # Get allocation value (0 if not in solution)
                alloc = solution.get((i, j), 0)
                ttk.Label(
                    grid_frame,
                    text=str(alloc),
                    font=("Arial", 9),
                    padding=5,
                    relief="ridge",
                    width=8,
                ).grid(row=i + 1, column=j + 1, sticky="nsew")

        # Configure grid weights to make cells expand
        for i in range(len(self.supply) + 1):
            grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.demand) + 1):
            grid_frame.grid_columnconfigure(j, weight=1)

    def display_simple_transport_table(self, parent):
        """Display a simple version of the transport problem table"""
        frame = ttk.LabelFrame(parent, text="Tableau de transport initial", padding=10)
        frame.pack(fill="x", pady=(15, 5))

        # Create a treeview widget
        tree = ttk.Treeview(frame)

        # Define columns (sources on rows, destinations on columns)
        columns = (
            ["Source/Dest"] + [f"D{j+1}" for j in range(len(self.demand))] + ["Offre"]
        )
        tree["columns"] = columns
        tree.column("#0", width=0, stretch=tk.NO)

        # Format columns
        tree.column("Source/Dest", anchor=tk.W, width=100)
        for col in columns[1:]:
            tree.column(col, anchor=tk.CENTER, width=80)

        # Create headings
        tree.heading("Source/Dest", text="Source/Dest", anchor=tk.W)
        for col in columns[1:]:
            tree.heading(col, text=col)

        # Add data rows
        for i in range(len(self.supply)):
            values = (
                [f"S{i+1}"]
                + [str(self.costs[i][j]) for j in range(len(self.demand))]
                + [str(self.supply[i])]
            )
            tree.insert("", tk.END, values=values)

        # Add demand row
        values = ["Demande"] + [str(d) for d in self.demand] + [str(sum(self.demand))]
        tree.insert("", tk.END, values=values)

        tree.pack(fill="x")

    def display_transport_table(self):
        """Display the transport problem data in a table format matching the image style"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create main container with white background
        container = ttk.Frame(self.viz_frame, style="White.TFrame")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        ttk.Label(
            container,
            text="Tableau de Transport",
            font=("Arial", 12, "bold"),
            foreground="#2c3e50",
            background="white",
        ).pack(anchor="w", pady=(0, 10))

        # Create frame for the table
        table_frame = ttk.Frame(container, style="White.TFrame")
        table_frame.pack(fill="x")

        # Create headers for destinations
        for j in range(len(self.demand)):
            header = ttk.Label(
                table_frame,
                text=f"D{j+1}",
                font=("Arial", 9, "bold"),
                padding=(5, 2),
                relief="ridge",
                width=8,
                anchor="center",
                background="#f0f0f0",  # Light gray background for headers
            )
            header.grid(row=0, column=j + 1, sticky="nsew")

        # Create supply header
        supply_header = ttk.Label(
            table_frame,
            text="Offre",
            font=("Arial", 9, "bold"),
            padding=(5, 2),
            relief="ridge",
            width=8,
            anchor="center",
            background="#f0f0f0",
        )
        supply_header.grid(row=0, column=len(self.demand) + 1, sticky="nsew")

        # Create rows for sources
        for i in range(len(self.supply)):
            # Source label with light blue background
            source_label = ttk.Label(
                table_frame,
                text=f"S{i+1}",
                font=("Arial", 9, "bold"),
                padding=(5, 2),
                relief="ridge",
                width=8,
                anchor="center",
                background="#e6f3ff",  # Light blue background for sources
            )
            source_label.grid(row=i + 1, column=0, sticky="nsew")

            # Cost values with white background
            for j in range(len(self.demand)):
                cost_label = ttk.Label(
                    table_frame,
                    text=str(self.costs[i][j]),
                    font=("Arial", 9),
                    padding=(5, 2),
                    relief="ridge",
                    width=8,
                    anchor="center",
                    background="white",
                )
                cost_label.grid(row=i + 1, column=j + 1, sticky="nsew")

            # Supply value with light blue background
            supply_label = ttk.Label(
                table_frame,
                text=str(self.supply[i]),
                font=("Arial", 9),
                padding=(5, 2),
                relief="ridge",
                width=8,
                anchor="center",
                background="#e6f3ff",
            )
            supply_label.grid(row=i + 1, column=len(self.demand) + 1, sticky="nsew")

        # Create demand row
        demand_label = ttk.Label(
            table_frame,
            text="Demande",
            font=("Arial", 9, "bold"),
            padding=(5, 2),
            relief="ridge",
            width=8,
            anchor="center",
            background="#f0f0f0",
        )
        demand_label.grid(row=len(self.supply) + 1, column=0, sticky="nsew")

        for j in range(len(self.demand)):
            d_label = ttk.Label(
                table_frame,
                text=str(self.demand[j]),
                font=("Arial", 9),
                padding=(5, 2),
                relief="ridge",
                width=8,
                anchor="center",
                background="white",
            )
            d_label.grid(row=len(self.supply) + 1, column=j + 1, sticky="nsew")

        # Total demand/supply cell
        total_label = ttk.Label(
            table_frame,
            text=str(sum(self.demand)),
            font=("Arial", 9),
            padding=(5, 2),
            relief="ridge",
            width=8,
            anchor="center",
            background="#f0f0f0",
        )
        total_label.grid(
            row=len(self.supply) + 1, column=len(self.demand) + 1, sticky="nsew"
        )

        # Configure grid weights
        for i in range(len(self.supply) + 2):
            table_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.demand) + 2):
            table_frame.grid_columnconfigure(j, weight=1)

        # Add some padding
        table_frame.grid(padx=5, pady=5)

        # Add summary information
        summary_frame = ttk.Frame(container, style="White.TFrame")
        summary_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(
            summary_frame,
            text=f"Nombre de sources: {len(self.supply)}",
            font=("Arial", 9),
            background="white",
        ).pack(side="left", padx=10)

        ttk.Label(
            summary_frame,
            text=f"Nombre de destinations: {len(self.demand)}",
            font=("Arial", 9),
            background="white",
        ).pack(side="left", padx=10)

        ttk.Label(
            summary_frame,
            text=f"Offre totale: {sum(self.supply)}",
            font=("Arial", 9),
            background="white",
        ).pack(side="left", padx=10)

        ttk.Label(
            summary_frame,
            text=f"Demande totale: {sum(self.demand)}",
            font=("Arial", 9),
            background="white",
        ).pack(side="left", padx=10)

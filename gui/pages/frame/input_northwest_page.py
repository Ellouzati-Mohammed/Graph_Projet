import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Visualisation.Programation_leaner.NorthWestPage import NorthwestPage

class InputNorthwestPage(tk.Frame):
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
            text="Algorithme du Coin Nord-Ouest",
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
        dialog.title("Saisie manuelle Coin Nord-Ouest")
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
            self.update_status("Exécution de l'algorithme du Coin Nord-Ouest...")

            # Supprimer le placeholder
            self.placeholder.pack_forget()

            # Créer les données pour NorthwestPage
            data = {
                'supply': self.supply,
                'demand': self.demand,
                'costs': self.costs
            }

            # Afficher les résultats avec NorthwestPage
            self.display_northwest_results(data)

            self.update_status("Algorithme du Coin Nord-Ouest exécuté avec succès")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Erreur lors du lancement de l'algorithme: {str(e)}"
            )
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def display_northwest_results(self, data):
       
        """Affiche les résultats avec la classe NorthwestPage"""
        # Effacer la visualisation précédente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Créer un cadre conteneur pour NorthwestPage
        container = ttk.Frame(self.viz_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialiser et afficher NorthwestPage dans le conteneur
        northwest_page = NorthwestPage(container)
        northwest_page.set_data(data)
        northwest_page.pack(fill="both", expand=True)

    def display_transport_table(self):
        """Display the transport problem data in a table format with visual representation"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(self.viz_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Data Table
        table_frame = ttk.Frame(notebook)
        notebook.add(table_frame, text="Tableau de données")

        # Create a treeview widget to display the table
        tree = ttk.Treeview(table_frame)

        # Define columns
        columns = (
            ["Source/Dest"] + [f"D{j+1}" for j in range(len(self.demand))] + ["Offre"]
        )
        tree["columns"] = columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column

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

        tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab 2: Compact Heatmap
        heatmap_frame = ttk.Frame(notebook)
        notebook.add(heatmap_frame, text="Matrice des Coûts")

        # Create a smaller figure for the heatmap
        fig, ax = plt.subplots(figsize=(6, 4))  # Reduced size
        fig.patch.set_facecolor("#f0f0f0")
        ax.set_facecolor("#f0f0f0")

        # Convert costs to numpy array
        cost_matrix = np.array(self.costs)

        # Create heatmap with color scale
        im = ax.imshow(cost_matrix, cmap="YlOrRd")

        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax, shrink=0.7)
        cbar.ax.set_ylabel("Coût", rotation=-90, va="bottom")

        # Show all ticks and label them
        ax.set_xticks(np.arange(len(self.demand)))
        ax.set_yticks(np.arange(len(self.supply)))
        ax.set_xticklabels([f"D{j+1}" for j in range(len(self.demand))])
        ax.set_yticklabels([f"S{i+1}" for i in range(len(self.supply))])

        # Rotate the tick labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Add text annotations
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                ax.text(
                    j,
                    i,
                    f"{self.costs[i][j]}",
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )  # Smaller font size

        ax.set_title("Matrice des Coûts", pad=10, fontsize=10)
        fig.tight_layout()

        # Embed the heatmap in tkinter
        canvas = FigureCanvasTkAgg(fig, master=heatmap_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Tab 3: Compact Transport Visualization
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="Schéma")

        # Create a smaller figure
        fig2, ax2 = plt.subplots(figsize=(6, 4))  # Reduced size
        fig2.patch.set_facecolor("#f0f0f0")
        ax2.set_facecolor("#f0f0f0")
        ax2.axis("off")

        # Draw sources (left side)
        for i, supply in enumerate(self.supply):
            ax2.text(-0.1, 0.9 - i * 0.2, f"S{i+1}", fontsize=10, ha="right")
            ax2.text(
                0,
                0.9 - i * 0.2,
                f"{supply}",
                fontsize=10,
                bbox=dict(facecolor="lightblue", alpha=0.5),
            )

        # Draw destinations (right side)
        for j, demand in enumerate(self.demand):
            ax2.text(0.9, 0.9 - j * 0.2, f"D{j+1}", fontsize=10)
            ax2.text(
                1.0,
                0.9 - j * 0.2,
                f"{demand}",
                fontsize=10,
                bbox=dict(facecolor="lightgreen", alpha=0.5),
            )

        # Draw cost matrix in the center (simplified)
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                ax2.text(
                    0.4 + j * 0.15,
                    0.9 - i * 0.2,
                    f"{self.costs[i][j]}",
                    fontsize=8,
                    ha="center",
                    va="center",
                )

        ax2.set_title("Problème de Transport", pad=10, fontsize=10)
        ax2.set_xlim(-0.2, 1.2)
        ax2.set_ylim(0, 1)

        canvas2 = FigureCanvasTkAgg(fig2, master=visual_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

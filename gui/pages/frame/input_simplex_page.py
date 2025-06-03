import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


class InputSimplexPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.c = []
        self.A = []
        self.b = []
        self.solution = None
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
            text="Algorithme du Simplexe",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Résolution de problème linéaire (PL)",
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
            "   - Fonction objectif (c) : Liste des coefficients\n"
            "   - Contraintes (A) : Matrice des coefficients\n"
            "   - Second membre (b) : Liste des valeurs\n\n"
            "3. Lancez l'algorithme pour résoudre le PL"
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
            right_panel, text="Résultats du Simplexe", style="TLabelframe"
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
        if not self.c or not self.A or not self.b:
            info_text = "Aucune donnée chargée"
        else:
            info_text = (
                f"• Variables: {len(self.c)}\n"
                f"• Contraintes: {len(self.b)}\n"
                f"• Fonction objectif: {' '.join(f'{coef:+}x{i}' for i, coef in enumerate(self.c, 1))}"
            )

        self.data_info_label.config(text=info_text)

    def reset_data(self):
        """Reset all data"""
        self.c = []
        self.A = []
        self.b = []
        self.solution = None

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

                if not all(key in data for key in ["c", "A", "b"]):
                    raise ValueError("Format JSON invalide")

                self.c = data["c"]
                self.A = data["A"]
                self.b = data["b"]

                self.validate_data()
                self.update_data_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.update_status(
                    f"Données JSON chargées: {len(self.c)} variables, {len(self.b)} contraintes"
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
                        "Le fichier CSV doit contenir au moins 3 lignes : une pour c, au moins une pour A, et une pour b."
                    )

                # Ligne 1 : coefficients c
                self.c = [float(x) for x in data[0]]

                # Lignes 2 à n-1 : contraintes A
                self.A = [[float(x) for x in row] for row in data[1:-1]]

                # Dernière ligne : second membre b
                self.b = [float(x) for x in data[-1]]

                self.validate_data()
                self.update_data_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.update_status(
                    f"Données CSV chargées: {len(self.c)} variables, {len(self.b)} contraintes"
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")
                self.update_status("Erreur lors de l'importation CSV")

    def show_manual_input(self):
        """Affiche la boîte de dialogue pour la saisie manuelle"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle Simplexe")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f0f0")

        # Main container
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Objective function input
        obj_frame = ttk.LabelFrame(
            main_frame,
            text="Fonction objectif (c) - Coefficients séparés par des virgules",
            style="TLabelframe",
        )
        obj_frame.pack(fill="x", pady=5)
        obj_entry = ttk.Entry(obj_frame)
        obj_entry.pack(fill="x", padx=5, pady=5)

        # Constraints input
        constr_frame = ttk.LabelFrame(
            main_frame,
            text="Contraintes (A) - Une ligne par contrainte, valeurs séparées par des virgules",
            style="TLabelframe",
        )
        constr_frame.pack(fill="both", expand=True, pady=5)
        constr_text = tk.Text(constr_frame, height=10, width=40)
        constr_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Right-hand side input
        b_frame = ttk.LabelFrame(
            main_frame,
            text="Second membre (b) - Valeurs séparées par des virgules",
            style="TLabelframe",
        )
        b_frame.pack(fill="x", pady=5)
        b_entry = ttk.Entry(b_frame)
        b_entry.pack(fill="x", padx=5, pady=5)

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
                dialog, obj_entry.get(), constr_text.get("1.0", "end-1c"), b_entry.get()
            ),
            style="Accent.TButton",
        ).pack(side="right", padx=5, fill="x", expand=True)

    def validate_manual_input(self, dialog, c_str, A_str, b_str):
        """Validate manual input data"""
        try:
            # Parse objective function
            c = [float(x.strip()) for x in c_str.split(",") if x.strip()]
            if not c:
                raise ValueError(
                    "Veuillez saisir au moins un coefficient pour la fonction objectif"
                )

            # Parse constraints matrix
            A = [
                [float(val.strip()) for val in line.split(",") if val.strip()]
                for line in A_str.strip().split("\n")
                if line.strip()
            ]
            if not A:
                raise ValueError("Veuillez saisir au moins une contrainte")

            # Parse right-hand side
            b = [float(x.strip()) for x in b_str.split(",") if x.strip()]
            if not b:
                raise ValueError(
                    "Veuillez saisir au moins une valeur pour le second membre"
                )

            # Validate dimensions
            if len(A) != len(b):
                raise ValueError(
                    "Le nombre de contraintes doit correspondre au nombre de valeurs du second membre"
                )

            if any(len(row) != len(c) for row in A):
                raise ValueError(
                    "Chaque contrainte doit avoir autant de coefficients que la fonction objectif"
                )

            self.c = c
            self.A = A
            self.b = b

            self.update_data_info()
            self.run_button.config(state="normal")
            dialog.destroy()
            messagebox.showinfo(
                "Succès",
                f"Problème créé avec {len(c)} variables et {len(b)} contraintes",
            )
            self.update_status(
                f"Données manuelles chargées: {len(c)} variables, {len(b)} contraintes"
            )

        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=dialog)
            self.update_status("Erreur dans la saisie manuelle")

    def validate_data(self):
        """Valide les données saisies pour le Simplexe"""
        if not self.c or not self.A or not self.b:
            raise ValueError("Toutes les données sont requises")

        if len(self.A) != len(self.b):
            raise ValueError(
                "Le nombre de contraintes doit correspondre au nombre de valeurs du second membre."
            )

        if any(len(row) != len(self.c) for row in self.A):
            raise ValueError(
                "Chaque contrainte doit avoir autant de coefficients que la fonction objectif."
            )

    def run_algorithm(self):
        """Lance l'algorithme avec les données saisies et affiche les résultats"""
        try:
            self.validate_data()
            self.update_status("Exécution de l'algorithme du Simplexe...")

            # Simulate solving the problem (replace with actual simplex implementation)
            self.solution = self.simulate_simplex()

            # Display results
            self.display_results()

            self.update_status("Algorithme du Simplexe exécuté avec succès")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Erreur lors du lancement de l'algorithme: {str(e)}"
            )
            self.update_status("Erreur lors de l'exécution de l'algorithme")

    def simulate_simplex(self):
        """Simulate simplex algorithm (replace with actual implementation)"""
        # This is just a placeholder - replace with your actual simplex implementation
        num_vars = len(self.c)
        num_constraints = len(self.b)

        # Create a dummy solution
        solution = {
            "optimal_value": sum(self.c) * 2,  # Just a dummy calculation
            "variables": {f"x{i+1}": self.c[i] * 0.5 for i in range(num_vars)},
            "status": "optimal",
            "iterations": num_constraints * 2,
            "reduced_costs": [round(c * 0.1, 2) for c in self.c],
            "shadow_prices": [round(b * 0.2, 2) for b in self.b],
        }

        return solution

    def display_results(self):
        """Display the simplex results with info on left and graph on right"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Main container with two columns
        main_container = ttk.Frame(self.viz_frame)
        main_container.pack(fill="both", expand=True)

        # Left panel for information (60% width)
        left_panel = ttk.Frame(main_container, width=int(self.winfo_width() * 0.6))
        left_panel.pack(side="left", fill="both", expand=True)

        # Right panel for graph (40% width)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)

        # Create scrollable area for left panel
        canvas = tk.Canvas(left_panel)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display optimal solution
        sol_frame = ttk.LabelFrame(
            scrollable_frame, text="Solution Optimale", style="TLabelframe"
        )
        sol_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(
            sol_frame,
            text=f"Valeur optimale: {self.solution['optimal_value']:.2f}",
            font=("Arial", 11, "bold"),
            foreground="#2b8a3e",
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Label(sol_frame, text="Variables:", font=("Arial", 9, "bold")).pack(
            anchor="w", padx=5
        )
        for var, val in self.solution["variables"].items():
            ttk.Label(sol_frame, text=f"{var} = {val:.4f}", font=("Arial", 9)).pack(
                anchor="w", padx=15
            )

        # Additional information
        info_frame = ttk.LabelFrame(
            scrollable_frame, text="Informations Complémentaires", style="TLabelframe"
        )
        info_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(
            info_frame, text=f"Statut: {self.solution['status']}", font=("Arial", 9)
        ).pack(anchor="w", padx=5)
        ttk.Label(
            info_frame,
            text=f"Itérations: {self.solution['iterations']}",
            font=("Arial", 9),
        ).pack(anchor="w", padx=5)

        ttk.Label(info_frame, text="Coûts réduits:", font=("Arial", 9, "bold")).pack(
            anchor="w", padx=5
        )
        for i, rc in enumerate(self.solution["reduced_costs"], 1):
            ttk.Label(info_frame, text=f"x{i}: {rc:.4f}", font=("Arial", 9)).pack(
                anchor="w", padx=15
            )

        ttk.Label(info_frame, text="Prix ombres:", font=("Arial", 9, "bold")).pack(
            anchor="w", padx=5
        )
        for i, sp in enumerate(self.solution["shadow_prices"], 1):
            ttk.Label(
                info_frame, text=f"Contrainte {i}: {sp:.4f}", font=("Arial", 9)
            ).pack(anchor="w", padx=15)

        # Create graph in right panel
        fig = plt.figure(figsize=(5, 4), facecolor="#f8f9fa")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#f8f9fa")

        iterations = range(1, self.solution["iterations"] + 1)
        values = [
            self.solution["optimal_value"] * (i / self.solution["iterations"])
            for i in iterations
        ]

        ax.plot(iterations, values, marker="o", color="#4a6baf", linewidth=1.5)
        ax.set_title("Évolution de la valeur objective", fontsize=10)
        ax.set_xlabel("Itérations", fontsize=8)
        ax.set_ylabel("Valeur", fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.tick_params(axis="both", which="major", labelsize=8)

        # Add some space around the plot
        fig.tight_layout(pad=2.0)

        # Embed the plot in right panel
        graph_frame = ttk.LabelFrame(
            right_panel, text="Visualisation", style="TLabelframe"
        )
        graph_frame.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Add some space at the bottom
        ttk.Frame(scrollable_frame, height=10).pack()

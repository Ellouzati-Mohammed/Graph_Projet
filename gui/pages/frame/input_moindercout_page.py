import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import numpy as np

class InputMoinderCoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Titre
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                              text="Algorithme du Moindre Coût", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Résolution de problème de transport",
                                 font=("Arial", 10))
        subtitle_label.pack(pady=2)
        
        # Frame pour les contrôles
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Boutons d'importation
        import_frame = ttk.LabelFrame(self.controls_frame, text="Importation des données")
        import_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(import_frame, text="Import JSON", 
                  command=self.import_json).pack(side="left", padx=5, pady=5)
        ttk.Button(import_frame, text="Import CSV", 
                  command=self.import_csv).pack(side="left", padx=5, pady=5)
        ttk.Button(import_frame, text="Saisie manuelle", 
                  command=self.show_manual_input).pack(side="left", padx=5, pady=5)
        
        # Frame pour les informations
        info_frame = ttk.LabelFrame(self, text="Informations")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        info_text = """
        • Import JSON : Importez les données depuis un fichier JSON
        • Import CSV : Importez les données depuis un fichier CSV
        • Saisie manuelle : Entrez les données manuellement
        
        Format attendu :
        - Offres (supply) : Liste des quantités disponibles
        - Demandes (demand) : Liste des quantités requises
        - Coûts (costs) : Matrice des coûts de transport
        
        Note : La somme des offres doit être égale à la somme des demandes
        L'algorithme du Moindre Coût sélectionne à chaque étape la cellule avec le coût le plus faible.
        """
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)
        
        # Variables pour stocker les données
        self.supply = []
        self.demand = []
        self.costs = []
        
        # Frame pour les boutons de navigation
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Bouton retour au menu
        back_button = ttk.Button(nav_frame, 
                               text="Retour au menu", 
                               command=lambda: self.controller.change_frame("menu"))
        back_button.pack(side="left", padx=5)
        
        # Bouton pour lancer l'algorithme
        self.run_button = ttk.Button(nav_frame, 
                                   text="Lancer l'algorithme", 
                                   command=self.run_algorithm,
                                   style="Accent.TButton")
        self.run_button.pack(side="right", padx=5)
        self.run_button.config(state="disabled")
        
        # Message d'aide
        help_label = ttk.Label(self, 
                             text="Veuillez importer ou saisir les données avant de lancer l'algorithme",
                             font=("Arial", 9, "italic"))
        help_label.pack(pady=5)

    def import_json(self):
        """Importe les données depuis un fichier JSON"""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if not all(key in data for key in ['supply', 'demand', 'costs']):
                    raise ValueError("Format JSON invalide")
                
                self.supply = data['supply']
                self.demand = data['demand']
                self.costs = data['costs']
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.run_button.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")

    def import_csv(self):
        """Importe les données depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)
                
                # Première ligne : offres
                self.supply = [float(x) for x in data[0] if x.strip() != '']
                
                # Deuxième ligne : demandes
                self.demand = [float(x) for x in data[1] if x.strip() != '']
                
                # Reste : matrice des coûts
                self.costs = [[float(x) for x in row] for row in data[2:]]
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données importées avec succès")
                self.run_button.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")

    def show_manual_input(self):
        """Affiche l'interface de saisie manuelle"""
        manual_window = tk.Toplevel(self)
        manual_window.title("Saisie manuelle")
        manual_window.geometry("600x400")
        
        # Frame pour les offres
        supply_frame = ttk.LabelFrame(manual_window, text="Offres")
        supply_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(supply_frame, text="Entrez les quantités disponibles (séparées par des virgules):").pack(pady=2)
        supply_entry = ttk.Entry(supply_frame, width=50)
        supply_entry.pack(pady=2)
        
        # Frame pour les demandes
        demand_frame = ttk.LabelFrame(manual_window, text="Demandes")
        demand_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(demand_frame, text="Entrez les quantités requises (séparées par des virgules):").pack(pady=2)
        demand_entry = ttk.Entry(demand_frame, width=50)
        demand_entry.pack(pady=2)
        
        # Frame pour les coûts
        costs_frame = ttk.LabelFrame(manual_window, text="Coûts")
        costs_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(costs_frame, text="Entrez la matrice des coûts (une ligne par source, valeurs séparées par des virgules):").pack(pady=2)
        costs_text = tk.Text(costs_frame, height=5, width=50)
        costs_text.pack(pady=2)
        
        def validate_and_save():
            try:
                # Récupérer et valider les offres
                self.supply = [float(x.strip()) for x in supply_entry.get().split(",")]
                
                # Récupérer et valider les demandes
                self.demand = [float(x.strip()) for x in demand_entry.get().split(",")]
                
                # Récupérer et valider les coûts
                costs_lines = costs_text.get("1.0", "end-1c").strip().split("\n")
                self.costs = [[float(x.strip()) for x in line.split(",")] for line in costs_lines]
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données validées avec succès")
                self.run_button.config(state="normal")
                manual_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la validation: {str(e)}")
        
        # Boutons de validation et d'annulation
        button_frame = ttk.Frame(manual_window)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(button_frame, 
                  text="Valider", 
                  command=validate_and_save,
                  style="Accent.TButton").pack(side="right", padx=5)
        
        ttk.Button(button_frame, 
                  text="Annuler", 
                  command=manual_window.destroy).pack(side="right", padx=5)

    def validate_data(self):
        """Valide les données saisies"""
        if not self.supply or not self.demand or not self.costs:
            raise ValueError("Toutes les données sont requises")
        
        if len(self.costs) != len(self.supply):
            raise ValueError("Le nombre de lignes de la matrice des coûts doit correspondre au nombre d'offres")
        
        if len(self.costs[0]) != len(self.demand):
            raise ValueError("Le nombre de colonnes de la matrice des coûts doit correspondre au nombre de demandes")
        
        if abs(sum(self.supply) - sum(self.demand)) > 1e-10:
            raise ValueError("La somme des offres doit être égale à la somme des demandes")

    def run_algorithm(self):
        """Lance l'algorithme avec les données saisies"""
        try:
            self.validate_data()
            self.controller.show_visualisation("moindre-Cout", {
                'supply': self.supply,
                'demand': self.demand,
                'costs': self.costs
            })
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du lancement de l'algorithme: {str(e)}") 
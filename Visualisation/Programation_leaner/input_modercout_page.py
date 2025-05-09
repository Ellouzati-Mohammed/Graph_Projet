import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class InputModerCoutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.lancer_algo_button.config(state='disabled')  # Désactive le bouton au démarrage

    def create_widgets(self):
        # Titre
        title_label = tk.Label(self, text="Méthode du Coût Minimum", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Description
        description = """
        La méthode du coût minimum est une approche gloutonne qui :
        - Commence par la cellule avec le coût le plus bas
        - Alloue la quantité maximale possible
        - Continue avec la cellule au coût le plus bas suivant
        - Répète jusqu'à ce que toutes les demandes soient satisfaites
        """
        desc_label = tk.Label(self, text=description, justify="left", wraplength=600)
        desc_label.pack(pady=10)

        # Frame pour la saisie des coûts
        costs_frame = tk.LabelFrame(self, text="Matrice des Coûts", padx=10, pady=5)
        costs_frame.pack(padx=10, pady=5, fill="x")

        # Création des entrées pour les coûts
        self.cost_entries = []
        for i in range(3):  # 3 sources
            row_entries = []
            for j in range(4):  # 4 destinations
                entry = ttk.Entry(costs_frame, width=8)
                entry.grid(row=i, column=j, padx=5, pady=2)
                row_entries.append(entry)
            self.cost_entries.append(row_entries)

        # Labels pour les sources et destinations
        for i in range(3):
            tk.Label(costs_frame, text=f"S{i+1}").grid(row=i, column=4, padx=5)
        for j in range(4):
            tk.Label(costs_frame, text=f"D{j+1}").grid(row=3, column=j, padx=5)

        # Frame pour la saisie des offres
        supply_frame = tk.LabelFrame(self, text="Offres (Sources)", padx=10, pady=5)
        supply_frame.pack(padx=10, pady=5, fill="x")
        
        self.supply_entries = []
        for i in range(3):
            entry = ttk.Entry(supply_frame, width=8)
            entry.pack(side="left", padx=5)
            self.supply_entries.append(entry)

        # Frame pour la saisie des demandes
        demand_frame = tk.LabelFrame(self, text="Demandes (Destinations)", padx=10, pady=5)
        demand_frame.pack(padx=10, pady=5, fill="x")
        
        self.demand_entries = []
        for i in range(4):
            entry = ttk.Entry(demand_frame, width=8)
            entry.pack(side="left", padx=5)
            self.demand_entries.append(entry)

        # Boutons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.valider_button = ttk.Button(button_frame, text="Valider", command=self.valider_donnees)
        self.valider_button.pack(side="left", padx=5)

        self.lancer_algo_button = ttk.Button(button_frame, text="Lancer l'algorithme", 
                                           command=self.lancer_algorithme, state='disabled')
        self.lancer_algo_button.pack(side="left", padx=5)

    def valider_donnees(self):
        try:
            # Récupération des coûts
            costs = []
            for row in self.cost_entries:
                cost_row = []
                for entry in row:
                    value = float(entry.get())
                    if value < 0:
                        raise ValueError("Les coûts ne peuvent pas être négatifs")
                    cost_row.append(value)
                costs.append(cost_row)

            # Récupération des offres
            supply = []
            for entry in self.supply_entries:
                value = float(entry.get())
                if value < 0:
                    raise ValueError("Les offres ne peuvent pas être négatives")
                supply.append(value)

            # Récupération des demandes
            demand = []
            for entry in self.demand_entries:
                value = float(entry.get())
                if value < 0:
                    raise ValueError("Les demandes ne peuvent pas être négatives")
                demand.append(value)

            # Vérification de l'équilibre
            total_supply = sum(supply)
            total_demand = sum(demand)
            if abs(total_supply - total_demand) > 0.001:  # Tolérance pour les erreurs d'arrondi
                raise ValueError(f"Le problème n'est pas équilibré. Offre totale: {total_supply}, Demande totale: {total_demand}")

            # Création du dictionnaire de données
            data = {
                'costs': costs,
                'supply': supply,
                'demand': demand
            }

            # Sauvegarde des données
            os.makedirs('data', exist_ok=True)
            with open('data/moderCoutData.json', 'w') as f:
                json.dump(data, f)

            messagebox.showinfo("Succès", "Données validées avec succès!")
            self.lancer_algo_button.config(state='normal')  # Active le bouton après validation

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def lancer_algorithme(self):
        try:
            # Vérification que les données existent
            if not os.path.exists('data/moderCoutData.json'):
                messagebox.showerror("Erreur", "Veuillez d'abord valider les données")
                return

            # Lecture des données
            with open('data/moderCoutData.json', 'r') as f:
                data = json.load(f)

            # Envoi des données à la page de visualisation
            self.parent.show_page("ModerCout", data)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}") 
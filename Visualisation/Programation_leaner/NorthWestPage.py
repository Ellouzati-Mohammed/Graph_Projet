import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from algorithms.pl.NorthWest import northwest_corner

class NorthwestPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None  # Pas de données par défaut
        self.afficher_northwest_depuis_data()  # Affiche au démarrage

    def set_data(self, data):
        print("Données reçues dans NorthwestPage:", data)  # Debug
        self.data = data  # Stocke les données de l'input
        self.afficher_northwest_depuis_data()  # Affiche avec les données de l'input

    def afficher_northwest_depuis_data(self):
        if not self.data:
            return
        supply = self.data['supply']
        demand = self.data['demand']
        costs = np.array(self.data['costs'])
        
        # Résolution
        success, message, alloc, total_cost = northwest_corner(supply, demand, costs)
        
        # Nettoyage précédente visualisation
        if self.canvas_widget:
            self.canvas_widget.destroy()

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Affichage des résultats textuels
        result_frame = tk.Frame(main_frame)
        result_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        result_text = "Résultats du transport:\n\n"
        result_text += f"Statut: {'Succès' if success else 'Erreur'}\n"
        result_text += f"Message: {message}\n"
        
        if success:
            result_text += f"\nCoût total: {total_cost:.2f}\n"
            result_text += "\nMatrice d'allocation:\n"
            for row in alloc:
                result_text += "  ".join(f"{x:.0f}" for x in row) + "\n"

        label = tk.Label(result_frame, text=result_text, justify="left",
                         font=("Courier", 12), bg="#f0f0f0")
        label.pack(padx=10, pady=10)

        # Visualisation matricielle
        if success:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.axis('off')
            
            # Création du tableau
            table = plt.table(
                cellText=alloc.astype(int),
                cellColours=[[('#e0f0ff' if alloc[i,j] > 0 else 'white') for j in range(alloc.shape[1])] for i in range(alloc.shape[0])],
                loc='center',
                cellLoc='center',
                colLabels=[f"D{j+1}" for j in range(alloc.shape[1])],
                rowLabels=[f"S{i+1}" for i in range(alloc.shape[0])]
            )
            
            table.scale(1, 2)
            table.set_fontsize(14)
            ax.set_title("Allocation des ressources", pad=20)

            # Intégration dans Tkinter
            canvas = FigureCanvasTkAgg(fig, master=main_frame)
            canvas.draw()
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
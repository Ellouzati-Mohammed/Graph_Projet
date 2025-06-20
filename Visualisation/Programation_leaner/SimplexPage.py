import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from algorithms.pl.Simplex import robust_simplex

class SimplexPage(tk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
        self.afficher_simplexe_depuis_data()

    def set_data(self, data):
        self.data = data
        self.afficher_simplexe_depuis_data()

    def afficher_simplexe_depuis_data(self):
        """Affiche la solution du simplexe à partir des données fournies."""
        if not self.data:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Aucune donnée à afficher.", ha='center', va='center', fontsize=12)
            self.ax.set_title("Résultats de l'Algorithme du Simplexe")
            self.ax.axis('off')
            self.canvas.draw()
            return

        results = robust_simplex(self.data)

        status = results.get("status", "error")
        message = results.get("message", "Une erreur est survenue.")
        solution = results.get("solution")
        optimal_value = results.get("optimal_value")
        
        self.ax.clear()

        if status == "optimal":
            # Afficher les résultats
            opt_type = self.data.get('optimization_type', 'max').upper()
            result_text = f"Solution Optimale Trouvée (Optimisation: {opt_type})\n\n"
            result_text += f"Valeur Optimale (Z): {optimal_value:.2f}\n"
            result_text += "Solution (X):\n"
            if solution:
                for i, val in enumerate(solution):
                    result_text += f"  x{i+1} = {val:.2f}\n"
            else:
                result_text += "  Aucune variable de décision dans la solution."
            
            self.ax.text(0.05, 0.95, result_text, ha='left', va='top', fontsize=11, wrap=True, family='monospace')

        else: # Covers infeasible, unbounded, error, etc.
            display_message = f"Résultat: {message}"
            self.ax.text(0.5, 0.5, display_message, ha='center', va='center', fontsize=12, wrap=True)

        self.ax.set_title("Résultats de l'Algorithme du Simplexe")
        self.ax.axis('off')
        self.canvas.draw()

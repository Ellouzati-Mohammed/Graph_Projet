import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from algorithms.pl.MoindreCout import moindre_cout

class MoindreCoutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.visualiser_moindre_cout()

    def visualiser_moindre_cout(self):
        # Données d'exemple (coûts, offre, demande)
        costs = np.array([
            [8, 5, 6],
            [15, 10, 12],
            [3, 9, 10]
        ])
        supply = np.array([150, 175, 275])
        demand = np.array([200, 100, 300])

        # Appliquer l'algorithme du Moindre Coût
        allocation, total_cost = moindre_cout(costs, supply.copy(), demand.copy())

        # Afficher les résultats
        if self.canvas_widget:
            self.canvas_widget.destroy()

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame pour les résultats textuels
        result_frame = tk.Frame(main_frame)
        result_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Affichage des résultats
        result_text = "Résultats du Moindre Coût:\n\n"
        result_text += f"Coût total: {total_cost:.2f}\n\n"
        result_text += "Matrice d'allocation:\n"
        for row in allocation:
            result_text += " ".join(f"{val:>5.0f}" for val in row) + "\n"

        label = tk.Label(result_frame, text=result_text, justify="left",
                        font=("Courier", 12), bg="#f0f0f0")
        label.pack(padx=10, pady=10)

        # Visualisation graphique (même pour 3+ clients)
        fig, ax = plt.subplots(figsize=(8, 6))
        self.plot_transport(allocation, costs, ax)
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def plot_transport(self, allocation, costs, ax):
        """Nouvelle visualisation adaptée à N clients."""
        n_fournisseurs, n_clients = allocation.shape
        
        # Créer un diagramme en barres empilées
        bottom = np.zeros(n_fournisseurs)
        colors = plt.cm.tab20(np.linspace(0, 1, n_clients))  # Palette pour les clients

        for j in range(n_clients):
            ax.bar(
                range(n_fournisseurs),
                allocation[:, j],
                bottom=bottom,
                label=f"Client {j+1}",
                color=colors[j]
            )
            bottom += allocation[:, j]

        ax.set_xticks(range(n_fournisseurs))
        ax.set_xticklabels([f"Fourn. {i+1}" for i in range(n_fournisseurs)])
        ax.set_ylabel("Quantité allouée")
        ax.set_title("Répartition des allocations par fournisseur")
        ax.legend(title="Clients", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
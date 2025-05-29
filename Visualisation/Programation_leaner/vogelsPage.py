import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from algorithms.pl.Vogels import vogels_approximation
from data.transport_data import vogel_costs, vogel_supply, vogel_demand

class VogelsApproximationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None
        self.afficher_vogel_depuis_data()



    def set_data(self, data):
        print("Données reçues dans vogelsPage:", data) 
        self.data = data
        self.afficher_vogel_depuis_data()

    def afficher_vogel_depuis_data(self):
        if not self.data:
            return
        costs = np.array(self.data['costs'])
        supply = np.array(self.data['supply'])
        demand = np.array(self.data['demand'])
        from algorithms.pl.Vogels import vogels_approximation

        allocation, total_cost = vogels_approximation(costs, supply.copy(), demand.copy())

        if self.canvas_widget:
            self.canvas_widget.destroy()

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        result_frame = tk.Frame(main_frame)
        result_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        result_text = "Résultats de la méthode de Vogel :\n\n"
        result_text += f"Coût total: {total_cost:.2f}\n\n"
        result_text += "Matrice d'allocation:\n"
        for row in allocation:
            result_text += " ".join(f"{val:>5.0f}" for val in row) + "\n"

        label = tk.Label(result_frame, text=result_text, justify="left",
                        font=("Courier", 12), bg="#f0f0f0")
        label.pack(padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(8, 6))
        self.plot_transport(allocation, costs, ax)
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def plot_transport(self, allocation, costs, ax):
        """Visualization adapted for N clients."""
        n_fournisseurs, n_clients = allocation.shape
        
        # Create stacked bar chart
        bottom = np.zeros(n_fournisseurs)
        colors = plt.cm.tab20(np.linspace(0, 1, n_clients))  # Color palette for clients

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
        ax.set_title("Répartition des allocations par fournisseur (Vogel)")
        ax.legend(title="Clients", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
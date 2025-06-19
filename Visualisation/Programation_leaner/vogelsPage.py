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

        # Title label
        title_label = tk.Label(result_frame, text="Résultats de l'algorithme", font=("Arial", 11, "bold"), anchor="w", bg="#f0f0f0")
        title_label.pack(anchor="w", pady=(0, 5))

        # Status and cost
        status_text = "Statut: Succès\nMessage: Solution trouvée\n\nCoût total: {:.2f}".format(total_cost)
        status_label = tk.Label(result_frame, text=status_text, font=("Arial", 10), anchor="w", justify="left", bg="#f0f0f0")
        status_label.pack(anchor="w", pady=(0, 10))

        # Allocation matrix as a grid of labels
        matrix_frame = tk.Frame(result_frame, bg="#f0f0f0")
        matrix_frame.pack(pady=(0, 10))

        n_rows, n_cols = allocation.shape
        # Header row
        tk.Label(matrix_frame, text="", bg="#f0f0f0").grid(row=0, column=0, padx=2, pady=2)
        for j in range(n_cols):
            tk.Label(matrix_frame, text=f"D{j+1}", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=j+1, padx=2, pady=2)
        # Data rows
        for i in range(n_rows):
            tk.Label(matrix_frame, text=f"S{i+1}", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=i+1, column=0, padx=2, pady=2)
            for j in range(n_cols):
                val = allocation[i, j]
                bg_color = "#dbefff" if val > 0 else "white"
                tk.Label(matrix_frame, text=f"{int(val)}", width=6, font=("Arial", 10), bg=bg_color, relief="solid", borderwidth=1).grid(row=i+1, column=j+1, padx=2, pady=2)

        # Plot on the right
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
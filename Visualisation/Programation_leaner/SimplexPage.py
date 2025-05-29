import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from algorithms.pl.Simplex import simplexe_max  # adapte le chemin si besoin

class SimplexePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_widget = None
        self.data = None
        self.afficher_simplexe_depuis_data()  # Pour stocker les données reçues

    def set_data(self, data):
        self.data = data
        self.afficher_simplexe_depuis_data()

    def afficher_simplexe_depuis_data(self):
        if not self.data:
            return
        c = self.data['c']
        A = self.data['A']
        b = self.data['b']
        from algorithms.pl.Simplex import simplexe_max
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        success, message, x, z = simplexe_max(c, A, b)
        print(message, x, z)

        if self.canvas_widget:
            self.canvas_widget.destroy()

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        result_frame = tk.Frame(main_frame)
        result_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        result_text = "Résultats du simplexe:\n\n"
        result_text += f"Statut: {'Optimal trouvé' if success else 'Echec'}\n"

        if success:
            result_text += f"Valeur optimale: {z:.2f}\n"
            result_text += "Solution optimale:\n"
            for i, val in enumerate(x):
                result_text += f"x{i+1} = {val:.2f}\n"
        else:
            result_text += f"Message: {message}\n"

        label = tk.Label(result_frame, text=result_text, justify="left",
                         font=("Courier", 12), bg="#f0f0f0")
        label.pack(padx=10, pady=10)

        # Optionnel : visualisation graphique si 2 variables
        if success and len(x) == 2:
            fig, ax = plt.subplots(figsize=(6, 6))
            x_vals = np.linspace(0, 500, 800)

            y_bounds = []
            max_x, max_y = 0, 0

            for i in range(len(A)):
                a1, a2 = A[i]
                if a2 != 0:
                    y = (b[i] - a1 * x_vals) / a2
                    ax.plot(x_vals, y, label=f"{a1}x1 + {a2}x2 ≤ {b[i]}")
                    y_bounds.append(y)
                    max_y = max(max_y, np.nanmax(y[y >= 0]))
                elif a1 != 0:
                    x_bound = b[i] / a1
                    ax.axvline(x=x_bound, label=f"x1 ≤ {x_bound:.2f}")
                    max_x = max(max_x, x_bound)

            # Ajustement des dimensions
            y_bounds_np = np.vstack([np.clip(y, 0, np.inf) for y in y_bounds])
            y_min = np.min(y_bounds_np, axis=0)
            ax.fill_between(x_vals, 0, y_min, where=(y_min >= 0), color='gray', alpha=0.3, label="Région admissible")

            opt_x, opt_y = x
            ax.plot(opt_x, opt_y, 'ro', markersize=10, label=f"Solution optimale ({opt_x:.2f}, {opt_y:.2f})")

            # Déterminer les limites dynamiquement
            max_x = max(max_x, opt_x) * 1.2
            max_y = max(max_y, opt_y) * 1.2
            ax.set_xlim(0, max(10, max_x))
            ax.set_ylim(0, max(10, max_y))

            ax.set_xlabel("x1")
            ax.set_ylabel("x2")
            ax.set_title("Visualisation du Problème Linéaire")
            ax.grid(True)
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=main_frame)
            canvas.draw()
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

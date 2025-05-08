import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from assets.styles.AlgoButton import button_style

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  

        buttons = [
            ("Welsh-Powell", self.controller.change_frame, "visualisation"),
            ("Simplex", self.controller.change_frame, "visualisation"),
            ("moindre-Cout", self.controller.change_frame, "visualisation"),
            ("Kruskal", self.controller.change_frame, "visualisation"),
            ("Djikstra", self.controller.change_frame, "visualisation"),
            ("vogels Approximation", self.controller.change_frame, "visualisation"),
            ("Bellman-Ford", self.controller.change_frame, "visualisation"),
            ("Ford-Fulkerson", self.controller.change_frame, "visualisation"),
            ("NorthWest", self.controller.change_frame, "visualisation"),
        ]

        for index, (label, command, msg) in enumerate(buttons): #lajout des button auu frame
            row = index // 3
            col = index % 3
            btn = tk.Button(
                self,
                text=label,
                **button_style,
                command=lambda m=msg,l=label : command(m,l)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
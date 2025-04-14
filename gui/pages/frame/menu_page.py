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
            ("Kruskal", self.controller.change_frame, "Kruskal"),
            ("North West", self.controller.change_frame, "North West"),
            ("Bouton 4", self.controller.change_frame, "visualisation"),
            ("Bouton 5", self.controller.change_frame, "Action pour le bouton 5"),
            ("Bouton 6", self.controller.change_frame, "Action pour le bouton 6"),
            ("Bouton 7", self.controller.change_frame, "frame2"),
        ]

        for index, (label, command, msg) in enumerate(buttons): #lajout des button auu frame
            row = index // 3
            col = index % 3
            btn = tk.Button(
                self,
                text=label,
                **button_style,
                command=lambda m=msg: command(m)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
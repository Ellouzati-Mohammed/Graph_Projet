import tkinter as tk
from tkinter import ttk
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
            ("Dijkstra", self.controller.change_frame, "input_dijkstra"),
            ("vogels Approximation", self.controller.change_frame, "visualisation"),
            ("Bellman-Ford", self.controller.change_frame, "visualisation"),
            ("Ford-Fulkerson", self.controller.change_frame, "visualisation"),
            ("NorthWest", self.controller.change_frame, "input_northwest"),
        ]

        for index, (label, command, msg) in enumerate(buttons):
            row = index // 3
            col = index % 3
            btn = tk.Button(
                self,
                text=label,
                **button_style,
                command=lambda m=msg, l=label: self.handle_button_click(m, l),
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

    def handle_button_click(self, frame_name, algo_name):
        """Gère le clic sur un bouton d'algorithme"""
        print(f"Bouton cliqué : {algo_name} -> {frame_name}")  # Debug
        self.controller.change_frame(frame_name, algo_name)

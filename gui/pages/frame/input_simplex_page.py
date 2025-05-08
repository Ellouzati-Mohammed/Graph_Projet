import tkinter as tk

class InputSimplexPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Interface de saisie/import pour Simplexe (à compléter)")
        label.pack(pady=20) 
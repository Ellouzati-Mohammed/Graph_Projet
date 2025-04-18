import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from assets.styles.AlgoButton import button_style
from gui.pages.frame.menu_page import MenuFrame
from gui.pages.frame.visualisation_page import VisualisationFrame


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("PL && Graph")

        self.container = tk.Frame(master)
        self.container.grid(padx=5, pady=5)

        # C réer les frames
        self.menu = MenuFrame(self.container, self)
        self.frame2 = tk.Frame(self.container)  
        self.visualisation = VisualisationFrame(self.container,self)

        # Par défaut, afficher menu
        self.menu.grid(row=0, column=0, padx=0, pady=0)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_frame(self, frame_name):
        for widget in self.container.winfo_children():
            widget.grid_forget()

        if frame_name == "menu":
            self.menu.grid(row=0, column=0, padx=20, pady=20)
        elif frame_name == "frame2":
            self.frame2.grid(row=0, column=0, padx=20, pady=20)
        elif frame_name == "visualisation":
            self.visualisation.grid(row=0, column=0, padx=20, pady=20)
            self.visualisation.visualiser_welshpowell_algo_graphe()
        elif frame_name == "simplexe":
            self.visualisation.grid(row=0, column=0, padx=20, pady=20)
            self.visualisation.visualiser_simplexe()

    def on_closing(self):
        print("La fenêtre est en train de se fermer.")  # Afficher un message de fermeture
        self.master.quit() 

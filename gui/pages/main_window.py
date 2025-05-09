import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from assets.styles.AlgoButton import button_style
from gui.pages.frame.menu_page import MenuFrame
from gui.pages.frame.visualisation_page import VisualisationFrame
from gui.pages.frame.input_dijkstra_page import InputDijkstraPage
from gui.pages.frame.input_northwest_page import InputNorthwestPage
from gui.pages.frame.input_simplex_page import InputSimplexPage


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("PL && Graph")
        
        # Configurer la grille principale
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(master)
        self.container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Créer les frames
        self.frames = {}
        self.frames["menu"] = MenuFrame(self.container, self)
        self.frames["input_dijkstra"] = InputDijkstraPage(self.container, self)
        self.frames["input_northwest"] = InputNorthwestPage(self.container, self)
        self.frames["input_simplex"] = InputSimplexPage(self.container, self)
        self.frames["visualisation"] = VisualisationFrame(self.container, self)

        # Par défaut, afficher menu
        self.show_frame("menu")

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, frame_name):
        """Affiche le frame demandé"""
        frame = self.frames.get(frame_name)
        if frame:
            # Cacher tous les frames
            for f in self.frames.values():
                f.grid_remove()
            # Afficher le frame demandé
            frame.grid(row=0, column=0, sticky="nsew")

    def change_frame(self, frame_name, algo_name=None):
        """Change de frame et gère les cas spéciaux"""
        print(f"Changement vers {frame_name} avec algo {algo_name}")  # Debug
        
        if frame_name in ["input_dijkstra", "input_northwest", "input_simplex"]:
            self.show_frame(frame_name)
            
        elif frame_name == "menu":
            self.show_frame("menu")
            
        elif frame_name == "visualisation" and algo_name:
            # Créer une nouvelle fenêtre pour la visualisation
            new_window = tk.Toplevel(self.master)
            new_window.title(f"Visualisation - {algo_name}")
            new_window.geometry("800x600")  # Taille par défaut
            
            # Configurer la grille de la nouvelle fenêtre
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_columnconfigure(0, weight=1)
            
            # Créer et afficher le frame de visualisation
            visualisation_frame = VisualisationFrame(new_window, self)
            visualisation_frame.grid(row=0, column=0, sticky="nsew")
            visualisation_frame.set_algorithm(algo_name)
    
    def show_visualisation(self, algo_name, data):
        """Affiche la visualisation avec les données"""
        # Créer une nouvelle fenêtre
        new_window = tk.Toplevel(self.master)
        new_window.title(f"Visualisation - {algo_name}")
        new_window.geometry("800x600")
        
        # Configurer la grille
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)
        
        # Créer et afficher le frame de visualisation
        visualisation_frame = VisualisationFrame(new_window, self)
        visualisation_frame.grid(row=0, column=0, sticky="nsew")
        visualisation_frame.set_algorithm(algo_name)
        visualisation_frame.set_data(data)
    
    def on_closing(self):
        print("La fenêtre est en train de se fermer.")
        self.master.quit() 

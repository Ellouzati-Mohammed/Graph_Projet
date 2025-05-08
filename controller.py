import tkinter as tk
from tkinter import ttk
from gui.pages.frame.menu_page import MenuFrame
from gui.pages.frame.input_dijkstra_page import InputDijkstraPage
from gui.pages.frame.visualisation_page import VisualisationFrame

class Controller:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        
        # Configurer la grille principale
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Créer toutes les pages
        self.create_frames()
        
        # Afficher le menu par défaut
        self.show_frame("menu")
    
    def create_frames(self):
        """Crée toutes les pages de l'application"""
        print("Création des frames...")  # Debug
        
        # Menu principal
        self.frames["menu"] = MenuFrame(self.root, self)
        self.frames["menu"].grid(row=0, column=0, sticky="nsew")
        print("Frame menu créé")  # Debug
        
        # Page d'input de Dijkstra
        self.frames["input_dijkstra"] = InputDijkstraPage(self.root, self)
        self.frames["input_dijkstra"].grid(row=0, column=0, sticky="nsew")
        print("Frame input_dijkstra créé")  # Debug
        
        # Page de visualisation
        self.frames["visualisation"] = VisualisationFrame(self.root, self)
        self.frames["visualisation"].grid(row=0, column=0, sticky="nsew")
        print("Frame visualisation créé")  # Debug
    
    def show_frame(self, frame_name):
        """Affiche la page demandée"""
        print(f"Tentative d'affichage de {frame_name}")  # Debug
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            print(f"Frame {frame_name} affiché")  # Debug
        else:
            print(f"ERREUR: Frame {frame_name} non trouvé")  # Debug
    
    def change_frame(self, frame_name, algo_name=None):
        """Change de page et initialise les données si nécessaire"""
        print(f"Changement de frame: {frame_name}, algo: {algo_name}")  # Debug
        if frame_name == "visualisation" and algo_name:
            # Si on va à la visualisation, on initialise avec le nom de l'algorithme
            self.frames["visualisation"].set_algorithm(algo_name)
        self.show_frame(frame_name)
    
    def show_visualisation(self, algo_name, data):
        """Affiche la page de visualisation avec les données"""
        print(f"Affichage visualisation pour {algo_name}")  # Debug
        self.frames["visualisation"].set_algorithm(algo_name)
        self.frames["visualisation"].set_data(data)
        self.show_frame("visualisation")

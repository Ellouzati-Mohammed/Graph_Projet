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

        # Créer les frames
        self.menu = MenuFrame(self.container, self)
        self.frame2 = tk.Frame(self.container)  
        self.visualisation = VisualisationFrame(self.container,self)

        # Par défaut, afficher menu
        self.menu.grid(row=0, column=0, padx=0, pady=0)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_frame(self, frame_name, algo_name=None):
        if frame_name == "menu":
            for widget in self.container.winfo_children():
                widget.grid_forget()
            self.menu.grid(row=0, column=0, padx=20, pady=20)
        
        elif frame_name == "visualisation" and algo_name:
            # Créer une nouvelle fenêtre
            new_window = tk.Toplevel(self.master)
            new_window.title(f"Visualisation - {algo_name}")

            visualisation_frame = VisualisationFrame(new_window, self)
            visualisation_frame.pack(fill="both", expand=True)
            visualisation_frame.afficher_algo(algo_name)


            #self.visualisation.visualiser_graphe()
            #self.visualisation.visualiser_Wech_Powell_graphe()
    
    def on_closing(self):
        print("La fenêtre est en train de se fermer.")  # Afficher un message de fermeture
        self.master.quit() 

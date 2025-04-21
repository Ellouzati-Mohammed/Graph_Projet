import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from data.graph_data import graph 
from Visualisation.graph.WelshPowellPage import WelshPowellPage
from Visualisation.graph.KruskalPage import KruskalPage
from Visualisation.graph.DjikstraPage import DijkstraPage
from Visualisation.Programation_leaner.SimplexPage import SimplexePage
from Visualisation.Programation_leaner.MoindreCoutPage import MoindreCoutPage
from Visualisation.Programation_leaner.vogelsPage import VogelsApproximationPage
from Visualisation.graph.BellmanFordPage import BellmanFordPage
from Visualisation.graph.FordFulkersonPage import FordFulkersonPage




class VisualisationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

    def afficher_algo(self, algo_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if algo_name == "Welsh-Powell":
            page = WelshPowellPage(self.content_frame)
        elif algo_name == "Kruskal":
            page = KruskalPage(self.content_frame)
        elif algo_name=="Djikstra":
            page= DijkstraPage(self.content_frame)
        elif algo_name=="Simplex":
            page= SimplexePage(self.content_frame)
        elif algo_name=="moindre-Cout":
            page= MoindreCoutPage(self.content_frame)
        elif algo_name=="vogels Approximation":
            page= VogelsApproximationPage(self.content_frame)
        elif algo_name=="Bellman-Ford":
            page= BellmanFordPage(self.content_frame)
        elif algo_name=="Ford-Fulkerson":
            page= FordFulkersonPage(self.content_frame)
            
        else:
            page = tk.Label(self.content_frame, text="Algorithme non disponible")


        page.pack(fill="both", expand=True)
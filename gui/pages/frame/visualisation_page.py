import tkinter as tk
from tkinter import ttk
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
from Visualisation.Programation_leaner.NorthWestPage import NorthwestPage
from Visualisation.graph.BellmanFordPage import BellmanFordPage
from Visualisation.graph.FordFulkersonPage import FordFulkersonPage


class VisualisationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Frame pour le titre
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)

        self.title_label = ttk.Label(
            title_frame, text="Visualisation", font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=5)

        # Frame pour le contenu
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Frame pour les contrôles
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=5)

        # Bouton retour au menu
        back_button = ttk.Button(
            self.controls_frame,
            text="Retour au menu",
            command=lambda: self.controller.change_frame("menu"),
        )
        back_button.pack(side="left", padx=5)

        # Variables pour stocker l'état
        self.current_algo = None
        self.current_data = None

    def set_algorithm(self, algo_name):
        """Définit l'algorithme à afficher"""
        self.current_algo = algo_name
        self.title_label.config(text=f"Visualisation - {algo_name}")
        self.afficher_algo(algo_name)

    def set_data(self, data):
        """Définit les données à visualiser"""
        self.current_data = data
        if self.current_algo:
            self.afficher_algo(self.current_algo)

    def afficher_algo(self, algo_name):
        """Affiche l'algorithme sélectionné avec les données"""
        # Nettoyer le contenu précédent
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if algo_name == "Welsh-Powell":
            page = WelshPowellPage(self.content_frame)
        elif algo_name == "Kruskal":
            page = KruskalPage(self.content_frame)
        elif algo_name == "Djikstra":
            page = DijkstraPage(self.content_frame)
        elif algo_name == "Simplex":
            page = SimplexePage(self.content_frame)
        elif algo_name == "moindre-Cout":
            page = MoindreCoutPage(self.content_frame)
        elif algo_name == "vogels Approximation":
            page = VogelsApproximationPage(self.content_frame)
        elif algo_name == "Bellman-Ford":
            page = BellmanFordPage(self.content_frame)
        elif algo_name == "Ford-Fulkerson":
            page = FordFulkersonPage(self.content_frame)
        elif algo_name == "NorthWest":
            page = NorthwestPage(self.content_frame)
        else:
            error_label = ttk.Label(
                self.content_frame,
                text="Erreur lors de l'affichage : Algorithme inconnu",
                font=("Arial", 12),
                foreground="red",
            )
            error_label.pack(pady=20)

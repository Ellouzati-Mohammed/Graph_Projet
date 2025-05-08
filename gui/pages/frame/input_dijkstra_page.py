import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from .algos.dijkstra_import import DijkstraImporter

class InputDijkstraPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        print("Initialisation de InputDijkstraPage")  # Debug
        self.controller = controller
        
        # Titre
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                              text="Algorithme de Dijkstra", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Trouve le plus court chemin entre deux sommets",
                                 font=("Arial", 10))
        subtitle_label.pack(pady=2)
        
        # Frame pour les contrôles
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Intégration de l'importer
        try:
            self.importer = DijkstraImporter(self.controls_frame, self)
            print("DijkstraImporter créé avec succès")  # Debug
        except Exception as e:
            print(f"Erreur lors de la création de DijkstraImporter: {str(e)}")  # Debug
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation: {str(e)}")
        
        # Frame pour les informations
        info_frame = ttk.LabelFrame(self, text="Informations")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        info_text = """
        • Import JSON : Importez un graphe depuis un fichier JSON
        • Import CSV : Importez un graphe depuis un fichier CSV
        • Saisie manuelle : Entrez les données du graphe manuellement
        
        Format attendu :
        - Sommets : Liste de noms (ex: A, B, C, D)
        - Matrice : Matrice d'adjacence avec les poids
        """
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)
        
        # Frame pour les boutons de navigation
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Bouton retour au menu
        back_button = ttk.Button(nav_frame, 
                               text="Retour au menu", 
                               command=lambda: self.controller.change_frame("menu"))
        back_button.pack(side="left", padx=5)
        
        # Bouton pour lancer l'algorithme
        self.run_button = ttk.Button(nav_frame, 
                                   text="Lancer l'algorithme", 
                                   command=self.run_algorithm,
                                   style="Accent.TButton")
        self.run_button.pack(side="right", padx=5)
        
        # Variables pour stocker les données du graphe
        self.sommets = []
        self.matrice = []
        self.edges = []  # Pour la saisie manuelle
        
        # Message d'aide
        help_label = ttk.Label(self, 
                             text="Veuillez importer ou saisir les données du graphe avant de lancer l'algorithme",
                             font=("Arial", 9, "italic"))
        help_label.pack(pady=5)
        
        print("InputDijkstraPage initialisée avec succès")  # Debug
    
    def set_graph_data(self, sommets, matrice):
        """Méthode appelée par l'importer pour définir les données du graphe"""
        print(f"Données reçues: {len(sommets)} sommets")  # Debug
        self.sommets = sommets
        self.matrice = matrice
        # Afficher un message de confirmation
        messagebox.showinfo("Données chargées", 
                          f"Graphe chargé avec succès!\n"
                          f"Nombre de sommets : {len(sommets)}\n"
                          f"Sommets : {', '.join(sommets)}")
    
    def run_algorithm(self):
        """Lance l'algorithme avec les données importées"""
        print("Tentative de lancement de l'algorithme")  # Debug
        
        # Vérifier si nous avons des données de saisie manuelle
        if self.edges:
            print(f"Utilisation des données de saisie manuelle: {len(self.edges)} arêtes")
            self.controller.show_visualisation("Dijkstra", self.edges)
            return
            
        # Sinon, vérifier les données de la matrice
        if not self.sommets or not self.matrice:
            messagebox.showwarning("Attention", 
                                 "Veuillez d'abord importer ou saisir les données du graphe")
            return
            
        # Convertir la matrice en liste d'arêtes
        edges = []
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets)):
                if self.matrice[i][j] != 0 and self.matrice[i][j] != float('inf'):
                    edges.append((self.sommets[i], self.sommets[j], self.matrice[i][j]))
        
        print(f"Données converties: {len(edges)} arêtes")  # Debug
        # Naviguer vers la page de visualisation avec les données
        self.controller.show_visualisation("Dijkstra", edges)
    
    def clear(self):
        """Nettoie l'interface"""
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(self.master, self.controller)

    def saisie_manuelle(self):
        """Affiche l'interface de saisie manuelle"""
        self.clear()
        
        # Frame pour la saisie
        input_frame = ttk.LabelFrame(self, text="Saisie des arêtes")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Champs de saisie
        ttk.Label(input_frame, text="Sommet de départ:").pack(pady=2)
        self.from_entry = ttk.Entry(input_frame)
        self.from_entry.pack(pady=2)
        
        ttk.Label(input_frame, text="Sommet d'arrivée:").pack(pady=2)
        self.to_entry = ttk.Entry(input_frame)
        self.to_entry.pack(pady=2)
        
        ttk.Label(input_frame, text="Poids:").pack(pady=2)
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.pack(pady=2)
        
        # Bouton d'ajout
        ttk.Button(input_frame, text="Ajouter l'arête", command=self.add_edge).pack(pady=5)
        
        # Liste des arêtes
        list_frame = ttk.LabelFrame(self, text="Arêtes ajoutées")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.edges_listbox = tk.Listbox(list_frame)
        self.edges_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Boutons de navigation
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(nav_frame, text="Retour", command=self.clear).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Valider", command=self.validate_manual_input).pack(side="right", padx=5)

    def add_edge(self):
        """Ajoute une arête à la liste"""
        try:
            f = self.from_entry.get().strip()
            t = self.to_entry.get().strip()
            w = float(self.weight_entry.get())
            
            if not f or not t:
                raise ValueError("Les sommets ne peuvent pas être vides")
            
            self.edges.append((f, t, w))
            self.edges_listbox.insert(tk.END, f"{f} -> {t} : {w}")
            
            # Vider les champs
            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e) if str(e) else "Le poids doit être un nombre")

    def validate_manual_input(self):
        """Valide la saisie manuelle et lance l'algorithme"""
        if not self.edges:
            messagebox.showwarning("Attention", "Veuillez ajouter au moins une arête")
            return
            
        print(f"Validation de la saisie manuelle: {len(self.edges)} arêtes")
        self.controller.show_visualisation("Dijkstra", self.edges)

    def importer_fichier(self):
        """Importe les données depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                edges = []
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        f, t, w = row['from'], row['to'], float(row['weight'])
                        edges.append((f, t, w))
                self.edges = edges
                messagebox.showinfo("Succès", f"{len(edges)} arêtes importées avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}") 
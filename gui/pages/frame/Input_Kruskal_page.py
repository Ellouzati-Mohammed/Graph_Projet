import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from algorithms.graph.Kruskal import kruskal

class InputKruskal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sommets = []
        self.matrice = []
        self.edges = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)
        title_label = ttk.Label(title_frame, 
                              text="Algorithme de Kruskal", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        subtitle_label = ttk.Label(title_frame,
                                 text="Arbre couvrant de poids minimal",
                                 font=("Arial", 10))
        subtitle_label.pack(pady=2)

        # Import section
        import_frame = ttk.LabelFrame(self, text="Importation des données")
        import_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(import_frame, text="Import JSON", 
                  command=self.import_json).pack(side="left", padx=5, pady=5)
        ttk.Button(import_frame, text="Import CSV", 
                  command=self.import_csv).pack(side="left", padx=5, pady=5)
        ttk.Button(import_frame, text="Saisie manuelle", 
                  command=self.show_manual_input).pack(side="left", padx=5, pady=5)

        # Info/help section
        info_frame = ttk.LabelFrame(self, text="Informations")
        info_frame.pack(fill="x", padx=10, pady=5)
        info_text = (
            "• Import JSON : Importez un graphe depuis un fichier JSON\n"
            "• Import CSV : Importez un graphe depuis un fichier CSV\n"
            "• Saisie manuelle : Entrez les données du graphe manuellement\n\n"
            "Format attendu :\n"
            "- Sommets : Liste de noms (ex: A, B, C, D)\n"
            "- Matrice : Matrice d'adjacence pondérée\n"
            "- Arêtes : Liste de triplets (ex: A-B-3) si manuel\n"
        )
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)

        # Message d'aide
        help_label = ttk.Label(self, text="Veuillez importer ou saisir les données du graphe avant de lancer l'algorithme", font=("Arial", 9, "italic"))
        help_label.pack(pady=5)

        # Navigation
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(nav_frame, text="Retour au menu", 
                  command=lambda: self.controller.change_frame("menu")).pack(side="left", padx=5)
        self.run_button = ttk.Button(nav_frame, 
                                   text="Lancer l'algorithme", 
                                   command=self.run_algorithm,
                                   state="disabled", style="Accent.TButton")
        self.run_button.pack(side="right", padx=5)

    def import_json(self):
        """Importe un graphe depuis un fichier JSON"""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if 'sommets' not in data or 'matrice' not in data:
                    raise ValueError("Format JSON invalide. Doit contenir 'sommets' et 'matrice'")
                
                self.sommets = data['sommets']
                self.matrice = data['matrice']
                self.edges = []
                
                # Convertit la matrice en liste d'arêtes
                for i in range(len(self.sommets)):
                    for j in range(len(self.sommets)):
                        poids = self.matrice[i][j]
                        if poids > 0 and i < j:  # Évite les doublons
                            self.edges.append((self.sommets[i], self.sommets[j], poids))
                
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", f"Graphe importé avec {len(self.sommets)} sommets")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import JSON: {str(e)}")
    
    def import_csv(self):
        """Importe un graphe depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                edges = []
                sommets = set()
                
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 3:
                            f, t, w = row[0], row[1], float(row[2])
                            edges.append((f, t, w))
                            sommets.add(f)
                            sommets.add(t)
                
                self.sommets = list(sommets)
                self.edges = edges
                
                # Crée la matrice d'adjacence
                n = len(self.sommets)
                self.matrice = [[0]*n for _ in range(n)]
                
                for f, t, w in edges:
                    i = self.sommets.index(f)
                    j = self.sommets.index(t)
                    self.matrice[i][j] = w
                    self.matrice[j][i] = w
                
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", f"Graphe importé avec {len(self.sommets)} sommets et {len(edges)} arêtes")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import CSV: {str(e)}")
    
    def show_manual_input(self):
        """Affiche la boîte de dialogue pour la saisie manuelle"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle du graphe")
        dialog.geometry("600x500")
        
        # Frame d'entrée
        input_frame = ttk.LabelFrame(dialog, text="Ajouter une arête pondérée")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Sommet 1
        ttk.Label(input_frame, text="Sommet 1:").grid(row=0, column=0, padx=5, pady=2)
        self.vertex1_entry = ttk.Entry(input_frame)
        self.vertex1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # Sommet 2
        ttk.Label(input_frame, text="Sommet 2:").grid(row=1, column=0, padx=5, pady=2)
        self.vertex2_entry = ttk.Entry(input_frame)
        self.vertex2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Poids
        ttk.Label(input_frame, text="Poids:").grid(row=2, column=0, padx=5, pady=2)
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        # Bouton d'ajout
        ttk.Button(input_frame, text="Ajouter", command=lambda: self.add_edge(dialog)).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Liste des arêtes
        list_frame = ttk.LabelFrame(dialog, text="Arêtes ajoutées")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.edges_listbox = tk.Listbox(list_frame)
        self.edges_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Boutons de navigation
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Valider", command=lambda: self.validate_manual_input(dialog)).pack(side="right", padx=5)
    
    def add_edge(self, dialog):
        """Ajoute une arête à la liste"""
        try:
            v1 = self.vertex1_entry.get().strip()
            v2 = self.vertex2_entry.get().strip()
            weight = self.weight_entry.get().strip()
            
            if not v1 or not v2 or not weight:
                raise ValueError("Tous les champs doivent être remplis")
            
            try:
                weight = float(weight)
            except ValueError:
                raise ValueError("Le poids doit être un nombre")
            
            if v1 == v2:
                raise ValueError("Une arête ne peut pas relier un sommet à lui-même")
            
            if weight <= 0:
                raise ValueError("Le poids doit être positif")
            
            # Vérifie les doublons
            for edge in self.edges:
                if (edge[0] == v1 and edge[1] == v2) or (edge[0] == v2 and edge[1] == v1):
                    raise ValueError(f"L'arête entre {v1} et {v2} existe déjà")
            
            self.edges.append((v1, v2, weight))
            self.edges_listbox.insert(tk.END, f"{v1} — {v2} (poids: {weight})")
            
            # Efface les champs
            self.vertex1_entry.delete(0, tk.END)
            self.vertex2_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=dialog)
    
    def validate_manual_input(self, dialog):
        """Valide la saisie manuelle et crée les données du graphe"""
        if not self.edges:
            messagebox.showwarning("Attention", "Veuillez ajouter au moins une arête", parent=dialog)
            return
        
        # Vérifie les doublons
        seen = set()
        for v1, v2, w in self.edges:
            edge = (min(v1, v2), max(v1, v2))
            if edge in seen:
                messagebox.showerror("Erreur", f"L'arête {v1}-{v2} est en double", parent=dialog)
                return
            seen.add(edge)
        
        # Récupère tous les sommets uniques
        sommets = set()
        for v1, v2, w in self.edges:
            sommets.add(v1)
            sommets.add(v2)
        
        self.sommets = list(sommets)
        
        # Crée la matrice d'adjacence
        n = len(self.sommets)
        self.matrice = [[0]*n for _ in range(n)]
        
        for v1, v2, w in self.edges:
            i = self.sommets.index(v1)
            j = self.sommets.index(v2)
            self.matrice[i][j] = w
            self.matrice[j][i] = w
        
        self.update_graph_info()
        self.run_button.config(state="normal")
        dialog.destroy()
        messagebox.showinfo("Succès", f"Graphe créé avec {len(self.sommets)} sommets et {len(self.edges)} arêtes")
    
    def update_graph_info(self):
        """Met à jour l'affichage des informations du graphe"""
        if not self.sommets:
            self.graph_info_label.config(text="Aucun graphe chargé")
        else:
            total_weight = sum(edge[2] for edge in self.edges) / 2  # Divisé par 2 car chaque arête est comptée deux fois
            self.graph_info_label.config(text=f"Graphe avec {len(self.sommets)} sommets\n"
                                          f"et {len(self.edges)} arêtes\n"
                                          f"Poids total: {total_weight:.2f}")
    
    def run_algorithm(self):
        """Exécute l'algorithme de Kruskal et visualise le graphe"""
        if not self.sommets or not self.matrice:
            messagebox.showwarning("Attention", "Veuillez d'abord importer ou saisir les données du graphe")
            return
        
        try:
            # Exécute l'algorithme de Kruskal
            mst_edges = kruskal(self.sommets, self.matrice)
            
            # Prépare les données pour la visualisation
            data = {
                'sommets': self.sommets,
                'matrice': self.matrice,
                'edges': self.edges,
                'mst_edges': mst_edges
            }
            
            # Envoie à la visualisation
            self.controller.show_visualisation("Kruskal", data)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def clear(self):
        """Nettoie la page et réinitialise"""
        self.sommets = []
        self.matrice = []
        self.edges = []
        self.update_graph_info()
        self.run_button.config(state="disabled")
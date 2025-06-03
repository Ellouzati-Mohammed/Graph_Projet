import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.FordFulkerson import fordFulkerson

class InputFordFulkersonPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.graph_data = {
            'nodes': [],
            'edges': [],
            'source': '',
            'sink': ''
        }
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)

        title_label = ttk.Label(title_frame,
                              text="Algorithme de Ford-Fulkerson",
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Calcul du flot maximum dans un réseau",
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
            "- nodes : Liste de noms (ex: A, B, C, D)\n"
            "- edges : Liste de triplets (ex: A, B, 10)\n"
            "- source/sink : Sommets source et puits\n"
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
        
        self.run_btn = ttk.Button(nav_frame, text="Lancer l'algorithme", 
                                command=self.launch_visualization,
                                style="Accent.TButton",
                                state="disabled")
        self.run_btn.pack(side="right", padx=5)
    
    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                required = ['nodes', 'edges', 'source', 'sink']
                if not all(k in data for k in required):
                    raise ValueError("Format JSON invalide")
                
                # Convertir les capacités en int
                data['edges'] = [[u, v, int(c)] for u, v, c in data['edges']]
                
                self.graph_data = data
                self.validate_data()
                messagebox.showinfo("Succès", "Données importées!")
                self.run_btn.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'import: {str(e)}")
    
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                
                if len(data) < 2:
                    raise ValueError("Fichier CSV incomplet")
                
                self.graph_data = {
                    'nodes': data[0],
                    'source': data[1][0],
                    'sink': data[1][1],
                    'edges': [[row[0], row[1], int(row[2])] for row in data[2:] if len(row) >= 3]
                }
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données importées!")
                self.run_btn.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'import: {str(e)}")
    
    def show_manual_input(self):
        input_window = tk.Toplevel(self)
        input_window.title("Saisie manuelle")
        
        # Noeuds
        ttk.Label(input_window, text="Noeuds (séparés par des virgules):").pack(pady=5)
        nodes_entry = ttk.Entry(input_window, width=40)
        nodes_entry.pack()
        
        # Source et Puits
        source_frame = ttk.Frame(input_window)
        source_frame.pack(pady=5)
        ttk.Label(source_frame, text="Source:").pack(side="left")
        source_entry = ttk.Entry(source_frame, width=15)
        source_entry.pack(side="left", padx=5)
        
        sink_frame = ttk.Frame(input_window)
        sink_frame.pack(pady=5)
        ttk.Label(sink_frame, text="Puits:").pack(side="left")
        sink_entry = ttk.Entry(sink_frame, width=15)
        sink_entry.pack(side="left", padx=5)
        
        # Arêtes
        ttk.Label(input_window, text="Arêtes (une par ligne, format: noeud1,noeud2,capacité):").pack(pady=5)
        edges_text = tk.Text(input_window, height=8, width=40)
        edges_text.pack()
        
        def validate():
            try:
                nodes = [n.strip() for n in nodes_entry.get().split(",")]
                source = source_entry.get().strip()
                sink = sink_entry.get().strip()
                
                edges = []
                for line in edges_text.get("1.0", "end-1c").split("\n"):
                    if line.strip():
                        parts = [p.strip() for p in line.split(",")]
                        if len(parts) != 3:
                            raise ValueError("Format d'arête invalide")
                        edges.append([parts[0], parts[1], int(parts[2])])
                
                self.graph_data = {
                    'nodes': nodes,
                    'edges': edges,
                    'source': source,
                    'sink': sink
                }
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données validées!")
                input_window.destroy()
                self.run_btn.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Données invalides: {str(e)}")
        
        ttk.Button(input_window, text="Valider", command=validate).pack(pady=10)
    
    def validate_data(self):
        """Valide les données du graphe"""
        if not self.graph_data['nodes']:
            raise ValueError("Aucun noeud spécifié")
        
        if self.graph_data['source'] not in self.graph_data['nodes']:
            raise ValueError("Source non trouvée dans les noeuds")
        
        if self.graph_data['sink'] not in self.graph_data['nodes']:
            raise ValueError("Puits non trouvé dans les noeuds")
        
        for edge in self.graph_data['edges']:
            if edge[0] not in self.graph_data['nodes'] or edge[1] not in self.graph_data['nodes']:
                raise ValueError(f"Arête {edge} référence un noeud inexistant")
            if not isinstance(edge[2], int):
                raise ValueError(f"Capacité doit être un nombre entier pour l'arête {edge}")

    def run_algorithm(self):
        """Exécute l'algorithme de Ford-Fulkerson et affiche le résultat"""
        if not self.graph_data['nodes'] or not self.graph_data['edges']:
            messagebox.showwarning("Attention", "Veuillez d'abord importer ou saisir les données du graphe")
            return
        
        try:
            if not self.graph_data['source']:
                raise ValueError("La source doit être spécifiée")
            if not self.graph_data['sink']:
                raise ValueError("Le puits doit être spécifié")
            if self.graph_data['source'] == self.graph_data['sink']:
                raise ValueError("La source et le puits doivent être différents")

            sommets = self.graph_data['nodes']
            n = len(sommets)
            matrice = [[0]*n for _ in range(n)]
            sommet_index = {s: i for i, s in enumerate(sommets)}
            for u, v, capacity in self.graph_data['edges']:
                i, j = sommet_index[u], sommet_index[v]
                matrice[i][j] = capacity

            data = {
                'sommets': sommets,
                'matrice': matrice,
                'source': self.graph_data['source'],
                'sink': self.graph_data['sink']
            }
            self.controller.show_visualization("Ford-Fulkerson", data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def launch_visualization(self):
        """Prépare les données et lance la visualisation"""
        self.run_algorithm()


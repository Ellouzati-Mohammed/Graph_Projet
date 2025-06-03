import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv

class InputBellmanFordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.graph_data = {
            'nodes': [],
            'edges': [],
            'start': '',
            'end': ''
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                              text="Algorithme de Bellman-Ford", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Calcul du plus court chemin avec poids négatifs",
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
            "- edges : Liste de triplets (ex: A, B, 3)\n"
            "- start/end : Sommets de départ et d'arrivée\n"
        )
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)
        
        # Message d'aide
        help_label = ttk.Label(self, 
                             text="Veuillez importer ou saisir les données du graphe avant de lancer l'algorithme", 
                             font=("Arial", 9, "italic"))
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
                
                required = ['nodes', 'edges', 'start', 'end']
                if not all(k in data for k in required):
                    raise ValueError("Format JSON invalide")
                
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
                
                nodes = [n.strip() for n in data[0] if n.strip()]
                start = data[1][0].strip()
                end = data[1][1].strip()
                
                edges = []
                for row in data[2:]:
                    if len(row) >= 3:
                        u, v, w = row[0].strip(), row[1].strip(), float(row[2])
                        edges.append([u, v, w])
                
                self.graph_data = {
                    'nodes': nodes,
                    'start': start,
                    'end': end,
                    'edges': edges
                }
                
                self.validate_data()
                messagebox.showinfo("Succès", "Données importées!")
                self.run_btn.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'import: {str(e)}")
    
    def show_manual_input(self):
        input_window = tk.Toplevel(self)
        input_window.title("Saisie manuelle Bellman-Ford")
        input_window.geometry("500x500")
        
        # Noeuds
        ttk.Label(input_window, text="Noeuds (séparés par des virgules):").pack(pady=5)
        self.nodes_entry = ttk.Entry(input_window, width=40)
        self.nodes_entry.pack()
        
        # Départ et Arrivée
        start_frame = ttk.Frame(input_window)
        start_frame.pack(pady=5)
        ttk.Label(start_frame, text="Noeud de départ:").pack(side="left")
        self.start_entry = ttk.Entry(start_frame, width=15)
        self.start_entry.pack(side="left", padx=5)
        
        end_frame = ttk.Frame(input_window)
        end_frame.pack(pady=5)
        ttk.Label(end_frame, text="Noeud d'arrivée:").pack(side="left")
        self.end_entry = ttk.Entry(end_frame, width=15)
        self.end_entry.pack(side="left", padx=5)
        
        # Arêtes
        ttk.Label(input_window, 
                 text="Arêtes (une par ligne, format: noeud1,noeud2,poids):").pack(pady=5)
        self.edges_text = tk.Text(input_window, height=10, width=40)
        self.edges_text.pack()
        
        # Exemple de données
        example_btn = ttk.Button(input_window, 
                               text="Remplir avec un exemple",
                               command=self.fill_example)
        example_btn.pack(pady=5)
        
        # Boutons de validation
        btn_frame = ttk.Frame(input_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Valider", 
                 command=self.validate_manual_input,
                 style="Accent.TButton").pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Annuler", 
                 command=input_window.destroy).pack(side="left", padx=5)
    
    def fill_example(self):
        """Remplit les champs avec un exemple de graphe"""
        self.nodes_entry.delete(0, tk.END)
        self.nodes_entry.insert(0, "A,B,C,D,E")
        
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, "A")
        
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, "E")
        
        self.edges_text.delete("1.0", tk.END)
        example_edges = "A,B,4\nA,C,2\nB,C,3\nB,D,2\nB,E,3\nC,B,1\nC,D,4\nC,E,5\nD,E,-1"
        self.edges_text.insert("1.0", example_edges)
    
    def validate_manual_input(self):
        try:
            nodes = [n.strip() for n in self.nodes_entry.get().split(",") if n.strip()]
            start = self.start_entry.get().strip()
            end = self.end_entry.get().strip()
            
            edges = []
            for line in self.edges_text.get("1.0", "end-1c").split("\n"):
                if line.strip():
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        raise ValueError("Format d'arête invalide")
                    edges.append([parts[0], parts[1], float(parts[2])])
            
            self.graph_data = {
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': end
            }
            
            self.validate_data()
            messagebox.showinfo("Succès", "Données validées!")
            self.run_btn.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Données invalides: {str(e)}")
    
    def validate_data(self):
        """Valide les données du graphe"""
        if not self.graph_data['nodes']:
            raise ValueError("Aucun noeud spécifié")
        
        if self.graph_data['start'] not in self.graph_data['nodes']:
            raise ValueError("Noeud de départ non trouvé dans les noeuds")
        
        if self.graph_data['end'] not in self.graph_data['nodes']:
            raise ValueError("Noeud d'arrivée non trouvé dans les noeuds")
        
        for edge in self.graph_data['edges']:
            if edge[0] not in self.graph_data['nodes'] or edge[1] not in self.graph_data['nodes']:
                raise ValueError(f"Arête {edge} référence un noeud inexistant")
            if edge[0] == edge[1]:
                raise ValueError(f"Boucle détectée sur le noeud {edge[0]}")
    
    def launch_visualization(self):
        """Passe à la visualisation avec les données"""
        # Transform data to expected format
        n = len(self.graph_data['nodes'])
        matrice = [[0]*n for _ in range(n)]
        sommet_index = {s: i for i, s in enumerate(self.graph_data['nodes'])}
        
        for u, v, poids in self.graph_data['edges']:
            i, j = sommet_index[u], sommet_index[v]
            matrice[i][j] = poids
        
        visualization_data = {
            'sommets': self.graph_data['nodes'],
            'matrice': matrice,
            'start': self.graph_data['start'],
            'end': self.graph_data['end']
        }
        
        self.controller.show_visualization("BellmanFord", visualization_data)
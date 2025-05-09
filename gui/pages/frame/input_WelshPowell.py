import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.Welsh_Powell import Welsh_Powell
from Visualisation.graph.WelshPowellPage import WelshPowellPage
class InputWelshPowell(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas_widget = None
        self.sommets = []
        self.matrice = []
        self.edges = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title Frame
        title_frame = ttk.Frame(self)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                              text="Algorithme de Welsh-Powell", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Coloration de graphes avec nombre minimal de couleurs",
                                 font=("Arial", 10))
        subtitle_label.pack(pady=2)
        
        # Main content frame
        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Input controls
        left_panel = ttk.Frame(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Import section
        import_frame = ttk.LabelFrame(left_panel, text="Importer un graphe")
        import_frame.pack(fill="x", padx=5, pady=5)

         # Reset button
        reset_frame = ttk.Frame(left_panel)
        reset_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(reset_frame, text="Réinitialiser les données", 
                 command=self.reset_data).pack(fill="x")
        
        ttk.Button(import_frame, text="Importer JSON", 
                  command=self.import_json).pack(fill="x", padx=5, pady=2)
        ttk.Button(import_frame, text="Importer CSV", 
                  command=self.import_csv).pack(fill="x", padx=5, pady=2)
        ttk.Button(import_frame, text="Saisie manuelle", 
                  command=self.show_manual_input).pack(fill="x", padx=5, pady=2)
        
        # Current graph info
        info_frame = ttk.LabelFrame(left_panel, text="Informations du graphe")
        info_frame.pack(fill="x", padx=5, pady=5)
        
        self.graph_info_label = ttk.Label(info_frame, text="Aucun graphe chargé")
        self.graph_info_label.pack(padx=5, pady=5)
        
        # Right panel - Visualization placeholder
        self.viz_frame = ttk.Frame(content_frame)
        self.viz_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Navigation Frame
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Button(nav_frame, text="Retour au menu", 
                  command=lambda: self.controller.change_frame("menu")).pack(side="left", padx=5)
        
        self.run_button = ttk.Button(nav_frame, 
                                   text="Lancer l'algorithme", 
                                   command=self.run_algorithm,
                                   state="disabled")
        self.run_button.pack(side="right", padx=5)
    
    def import_json(self):
        """Import graph from JSON file"""
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
                
                # Convert matrix to edges
                for i in range(len(self.sommets)):
                    for j in range(len(self.sommets)):
                        if self.matrice[i][j] == 1 and i < j:
                            self.edges.append((self.sommets[i], self.sommets[j]))
                
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", f"Graphe importé avec {len(self.sommets)} sommets")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import JSON: {str(e)}")
    
    def import_csv(self):
        """Import graph from CSV file"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                edges = []
                sommets = set()
                
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 2:
                            f, t = row[0], row[1]
                            edges.append((f, t))
                            sommets.add(f)
                            sommets.add(t)
                
                self.sommets = list(sommets)
                self.edges = edges
                
                # Create adjacency matrix
                n = len(self.sommets)
                self.matrice = [[0]*n for _ in range(n)]
                
                for f, t in edges:
                    i = self.sommets.index(f)
                    j = self.sommets.index(t)
                    self.matrice[i][j] = 1
                    self.matrice[j][i] = 1
                
                self.update_graph_info()
                self.run_button.config(state="normal")
                messagebox.showinfo("Succès", f"Graphe importé avec {len(self.sommets)} sommets et {len(edges)} arêtes")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import CSV: {str(e)}")
    
    def show_manual_input(self):
        """Show manual input dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Saisie manuelle du graphe")
        dialog.geometry("500x400")
        
        # Input Frame
        input_frame = ttk.LabelFrame(dialog, text="Ajouter une arête")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Vertex 1
        ttk.Label(input_frame, text="Sommet 1:").grid(row=0, column=0, padx=5, pady=2)
        self.vertex1_entry = ttk.Entry(input_frame)
        self.vertex1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # Vertex 2
        ttk.Label(input_frame, text="Sommet 2:").grid(row=1, column=0, padx=5, pady=2)
        self.vertex2_entry = ttk.Entry(input_frame)
        self.vertex2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Add button
        ttk.Button(input_frame, text="Ajouter", command=lambda: self.add_edge(dialog)).grid(row=2, column=0, columnspan=2, pady=5)
        
        # List of edges
        list_frame = ttk.LabelFrame(dialog, text="Arêtes ajoutées")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.edges_listbox = tk.Listbox(list_frame)
        self.edges_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Navigation buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Valider", command=lambda: self.validate_manual_input(dialog)).pack(side="right", padx=5)
    def reset_data(self):
        """Réinitialise toutes les données du graphe"""
        self.sommets = []
        self.matrice = []
        self.edges = []
        
        # Efface la visualisation si elle existe
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None
        
        # Met à jour l'affichage des informations
        self.update_graph_info()
        
        # Désactive le bouton d'exécution
        self.run_button.config(state="disabled")
        
        messagebox.showinfo("Réinitialisation", "Toutes les données ont été réinitialisées")

    def add_edge(self, dialog):
        """Add an edge to the list"""
        try:
            v1 = self.vertex1_entry.get().strip()
            v2 = self.vertex2_entry.get().strip()
            
            if not v1 or not v2:
                raise ValueError("Les noms des sommets ne peuvent pas être vides")
            
            if v1 == v2:
                raise ValueError("Une arête ne peut pas relier un sommet à lui-même")
            
            # Check for duplicate edges
            if (v1, v2) in self.edges or (v2, v1) in self.edges:
                raise ValueError(f"L'arête entre {v1} et {v2} existe déjà")
            
            self.edges.append((v1, v2))
            self.edges_listbox.insert(tk.END, f"{v1} — {v2}")
            
            # Clear fields
            self.vertex1_entry.delete(0, tk.END)
            self.vertex2_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=dialog)
    
    def validate_manual_input(self, dialog):
        """Validate manual input and create graph data"""
        if not self.edges:
            messagebox.showwarning("Attention", "Veuillez ajouter au moins une arête", parent=dialog)
            return
        
        # Check for duplicate edges
        seen = set()
        for v1, v2 in self.edges:
            edge = (min(v1, v2), max(v1, v2))
            if edge in seen:
                messagebox.showerror("Erreur", f"L'arête {v1}-{v2} est en double", parent=dialog)
                return
            seen.add(edge)
        
        # Get all unique vertices
        sommets = set()
        for v1, v2 in self.edges:
            sommets.add(v1)
            sommets.add(v2)
        
        self.sommets = list(sommets)
        
        # Create adjacency matrix
        n = len(self.sommets)
        self.matrice = [[0]*n for _ in range(n)]
        
        for v1, v2 in self.edges:
            i = self.sommets.index(v1)
            j = self.sommets.index(v2)
            self.matrice[i][j] = 1
            self.matrice[j][i] = 1
        
        self.update_graph_info()
        self.run_button.config(state="normal")
        dialog.destroy()
        messagebox.showinfo("Succès", f"Graphe créé avec {len(self.sommets)} sommets et {len(self.edges)} arêtes")
    
    def update_graph_info(self):
        """Update the graph information display"""
        if not self.sommets:
            self.graph_info_label.config(text="Aucun graphe chargé")
        else:
            self.graph_info_label.config(text=f"Graphe avec {len(self.sommets)} sommets\n"
                                          f"et {len(self.edges)} arêtes")
    
    def run_algorithm(self):
        """Run Welsh-Powell algorithm and visualize the graph"""
        if not self.sommets or not self.matrice:
            messagebox.showwarning("Attention", "Veuillez d'abord importer ou saisir les données du graphe")
            return
        
        try:
            # Run Welsh-Powell algorithm
            colored_vertices = Welsh_Powell(self.sommets, self.matrice)
            
            # Create graph visualization
            self.visualize_graph(colored_vertices)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def visualize_graph(self, colored_vertices):
        """Visualize the colored graph"""
        if self.canvas_widget:
            self.canvas_widget.destroy()
        
        G = nx.Graph()
        G.add_nodes_from(self.sommets)
        
        # Add edges
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets)):
                if self.matrice[i][j] > 0 and i < j:
                    G.add_edge(self.sommets[i], self.sommets[j])
        
        # Create color map
        color_map = []
        for sommet in self.sommets:
            index = self.sommets.index(sommet)
            for colored in colored_vertices:
                if colored[0] == index:
                    color_map.append(colored[1])
                    break
        
        fig = plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=800, font_weight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    def clear(self):
        """Clear the page and reinitialize"""
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None
        
        self.sommets = []
        self.matrice = []
        self.edges = []
        self.update_graph_info()
        self.run_button.config(state="disabled")

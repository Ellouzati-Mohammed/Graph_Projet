import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from algorithms.graph.welsh_powell import welsh_powell

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
        
        # Right panel - Visualization
        right_panel = ttk.Frame(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # Visualization placeholder
        self.viz_frame = ttk.Frame(right_panel)
        self.viz_frame.grid(row=1, column=0, sticky="nsew")
        
        # Navigation Frame
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Button(nav_frame, text="Retour au menu", 
                  command=lambda: self.controller.change_frame("menu")).pack(side="left", padx=5)
        
        self.run_button = ttk.Button(nav_frame, 
                                   text="Lancer l'algorithme", 
                                   command=self.run_algorithm,
                                   style="Accent.TButton")
        self.run_button.pack(side="right", padx=5)
        self.run_button.config(state="disabled")
    
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
                        if self.matrice[i][j] == 1 and i < j:  # Avoid duplicate edges
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
    
    def add_edge(self, dialog):
        """Add an edge to the list"""
        try:
            v1 = self.vertex1_entry.get().strip()
            v2 = self.vertex2_entry.get().strip()
            
            if not v1 or not v2:
                raise ValueError("Les noms des sommets ne peuvent pas être vides")
            
            if v1 == v2:
                raise ValueError("Une arête ne peut pas relier un sommet à lui-même")
            
            # Add to edges (both directions for undirected graph)
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
            colored_vertices = welsh_powell(self.sommets, self.matrice)
            
            # Create graph visualization
            self.visualize_graph(colored_vertices)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def visualize_graph(self, colored_vertices):
        """Visualize the graph with coloring"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        G = nx.Graph()
        
        # Add nodes with color attributes
        color_map = {}
        for vertex, color in colored_vertices:
            G.add_node(vertex)
            color_map[vertex] = color
        
        # Add edges
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets)):
                if self.matrice[i][j] == 1 and i < j:  # Avoid duplicate edges
                    G.add_edge(self.sommets[i], self.sommets[j])
        
        # Create figure
        fig, ax = plt.subplots(figsize=(6, 5))
        pos = nx.spring_layout(G, seed=42)  # Consistent layout
        
        # Get colors for nodes
        node_colors = [color_map[node] for node in G.nodes()]
        
        # Draw the graph
        nx.draw(G, pos, ax=ax, with_labels=True,
                node_color=node_colors,
                node_size=700,
                font_size=10,
                font_weight="bold",
                cmap=plt.cm.tab20)  # Using a colormap with 20 distinct colors
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add legend for colors
        unique_colors = set(color_map.values())
        legend_text = f"Nombre de couleurs utilisées: {len(unique_colors)}"
        ttk.Label(self.viz_frame, text=legend_text, font=("Arial", 10, "bold")).pack(pady=5)
    
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
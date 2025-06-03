import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import csv
import numpy as np
from typing import List, Dict, Tuple, Optional

class DijkstraImporter:
    def __init__(self, parent_frame: tk.Frame, algo_instance):
        self.parent_frame = parent_frame
        self.algo_instance = algo_instance
        self.setup_import_buttons()
        
    def setup_import_buttons(self):
        """Configure les boutons d'importation dans le frame parent"""
        # Frame principal pour l'importation
        import_frame = ttk.LabelFrame(self.parent_frame, text="Importation des données")
        import_frame.pack(fill="x", padx=5, pady=5)
        
        # Frame pour les boutons
        buttons_frame = ttk.Frame(import_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Style pour les boutons
        style = ttk.Style()
        style.configure("Import.TButton", padding=5)
        
        # Boutons d'importation avec icônes
        json_button = ttk.Button(buttons_frame, 
                               text="Import JSON", 
                               command=self.import_from_json,
                               style="Import.TButton")
        json_button.pack(side="left", padx=5, pady=5)
        
        csv_button = ttk.Button(buttons_frame, 
                              text="Import CSV", 
                              command=self.import_from_csv,
                              style="Import.TButton")
        csv_button.pack(side="left", padx=5, pady=5)
        
        manual_button = ttk.Button(buttons_frame, 
                                 text="Saisie manuelle", 
                                 command=self.open_manual_entry,
                                 style="Import.TButton")
        manual_button.pack(side="left", padx=5, pady=5)
        
        # Ajouter des tooltips
        self.create_tooltip(json_button, "Importer un graphe depuis un fichier JSON")
        self.create_tooltip(csv_button, "Importer un graphe depuis un fichier CSV")
        self.create_tooltip(manual_button, "Saisir manuellement les données du graphe")
    
    def create_tooltip(self, widget, text):
        """Crée un tooltip pour un widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, 
                            background="#ffffe0", 
                            relief="solid", 
                            borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind("<Leave>", lambda e: hide_tooltip())
        
        widget.bind("<Enter>", show_tooltip)
    
    def import_from_json(self):
        """Importe les données depuis un fichier JSON"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not self.validate_data(data):
                return
                
            self.algo_instance.set_graph_data(data["sommets"], data["matrice"])
            
        except json.JSONDecodeError:
            messagebox.showerror("Erreur", "Le fichier JSON est invalide")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'importation: {str(e)}")
    
    def import_from_csv(self):
        """Importe les données depuis un fichier CSV"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows or len(rows) < 2:
                    raise ValueError("Fichier CSV vide ou incomplet")
                # Si la première case est vide, on a une colonne d'index
                if rows[0][0] == '':
                    sommets = [s.strip() for s in rows[0][1:] if s.strip()]
                    matrice = []
                    for row in rows[1:]:
                        matrice.append([float(val) if val.strip() != '' else float('inf') for val in row[1:]])
                else:
                    sommets = [s.strip() for s in rows[0] if s.strip()]
                    matrice = []
                    for row in rows[1:]:
                        matrice.append([float(val) if val.strip() != '' else float('inf') for val in row])
                data = {
                    "sommets": sommets,
                    "matrice": matrice
                }
                if not self.validate_data(data):
                    return
                self.algo_instance.set_graph_data(sommets, matrice)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'importation: {str(e)}")
    
    def open_manual_entry(self):
        """Ouvre la fenêtre de saisie manuelle"""
        manual_window = tk.Toplevel(self.parent_frame)
        manual_window.title("Saisie manuelle des données")
        manual_window.geometry("600x400")
        
        # Style
        style = ttk.Style()
        style.configure("Manual.TLabel", padding=5)
        style.configure("Manual.TEntry", padding=5)
        
        # Frame pour la saisie des sommets
        sommets_frame = ttk.LabelFrame(manual_window, text="Sommets", style="Manual.TLabel")
        sommets_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(sommets_frame, 
                 text="Entrez les noms des sommets (séparés par des virgules):",
                 style="Manual.TLabel").pack(padx=5, pady=5)
        
        sommets_entry = ttk.Entry(sommets_frame, width=50, style="Manual.TEntry")
        sommets_entry.pack(padx=5, pady=5)
        sommets_entry.insert(0, "A, B, C, D")  # Exemple par défaut
        
        # Frame pour la saisie de la matrice
        matrice_frame = ttk.LabelFrame(manual_window, text="Matrice d'adjacence")
        matrice_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(matrice_frame, 
                 text="Entrez la matrice d'adjacence (une ligne par ligne, valeurs séparées par des virgules):",
                 style="Manual.TLabel").pack(padx=5, pady=5)
        
        matrice_text = tk.Text(matrice_frame, height=10, width=50)
        matrice_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Exemple de matrice par défaut
        example_matrix = """0, 2, 4, 0
2, 0, 1, 3
4, 1, 0, 5
0, 3, 5, 0"""
        matrice_text.insert("1.0", example_matrix)
        
        def validate_and_save():
            try:
                # Récupérer et valider les sommets
                sommets = [s.strip() for s in sommets_entry.get().split(",") if s.strip()]
                if not sommets:
                    raise ValueError("Aucun sommet n'a été saisi")
                
                # Récupérer et valider la matrice
                matrice_lines = matrice_text.get("1.0", "end-1c").strip().split("\n")
                matrice = []
                for line in matrice_lines:
                    row = [float(val) if val.strip() != '' else float('inf') for val in line.split(",")]
                    matrice.append(row)
                
                data = {
                    "sommets": sommets,
                    "matrice": matrice
                }
                
                if not self.validate_data(data):
                    return
                
                self.algo_instance.set_graph_data(sommets, matrice)
                manual_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la validation: {str(e)}")
        
        # Boutons de validation et d'annulation
        button_frame = ttk.Frame(manual_window)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(button_frame, 
                  text="Valider", 
                  command=validate_and_save,
                  style="Accent.TButton").pack(side="right", padx=5)
        
        ttk.Button(button_frame, 
                  text="Annuler", 
                  command=manual_window.destroy).pack(side="right", padx=5)
    
    def validate_data(self, data: Dict) -> bool:
        """Valide les données importées"""
        try:
            # Vérifier la présence des clés requises
            if "sommets" not in data or "matrice" not in data:
                raise ValueError("Format de données invalide: 'sommets' et 'matrice' sont requis")
            
            sommets = data["sommets"]
            matrice = data["matrice"]
            
            # Vérifier que les sommets sont des strings
            if not all(isinstance(s, str) for s in sommets):
                raise ValueError("Les sommets doivent être des chaînes de caractères")
            
            # Vérifier que la matrice est carrée
            n = len(sommets)
            if not all(len(row) == n for row in matrice) or len(matrice) != n:
                raise ValueError("La matrice doit être carrée et correspondre au nombre de sommets")
            
            # Vérifier que les poids sont numériques et ≥ 0
            for i in range(n):
                for j in range(n):
                    if matrice[i][j] != float('inf') and (not isinstance(matrice[i][j], (int, float)) or matrice[i][j] < 0):
                        raise ValueError(f"Les poids doivent être des nombres positifs ou inf (ligne {i+1}, colonne {j+1})")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erreur de validation", str(e))
            return False
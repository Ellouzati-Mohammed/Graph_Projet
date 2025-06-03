import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from gui.pages.frame.Input_Kruskal_page import InputKruskal
from gui.pages.frame.menu_page import MenuFrame
from gui.pages.frame.visualisation_page import VisualisationFrame
from gui.pages.frame.input_dijkstra_page import InputDijkstraPage
from gui.pages.frame.input_northwest_page import InputNorthwestPage
from gui.pages.frame.input_simplex_page import InputSimplexPage
from gui.pages.frame.input_vogels_page import InputVogelsPage
from gui.pages.frame.input_moindercout_page import InputMoinderCoutPage
from gui.pages.frame.input_WelshPowell import InputWelshPowell
from gui.pages.frame.Input_FordFulkerson_Page import InputFordFulkersonPage
from gui.pages.frame.input_BellmanFord_page import InputBellmanFordPage


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padding=(5, 2),
        )
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.current_frame = None

        # Blue-themed color scheme
        self.bg_color = "#f0f8ff"  # Alice blue background
        self.primary_color = "#1e3f66"  # Dark blue for titles
        self.secondary_color = "#3a7ca5"  # Medium blue for accents
        self.button_color = "#4682b4"  # Steel blue for buttons
        self.button_hover = "#5f9ea0"  # Cadet blue for button hover
        self.button_active = "#2f6690"  # Darker blue for active buttons
        self.text_color = "#333333"
        self.highlight_color = "#d9e6f2"

        master.title("Visualisateur d'Algorithmes")
        master.geometry("1000x800")
        master.configure(bg=self.bg_color)

        # Configure styles
        self.configure_styles()

        # Main container
        self.main_container = ttk.Frame(master)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with logos
        self.create_header()

        # Content area
        self.content_container = ttk.Frame(self.main_container)
        self.content_container.pack(fill="both", expand=True)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Footer
        self.create_footer()

        # Create frames
        self.frames = {}
        self.create_frames()

        # Show initial frame
        self.show_frame("menu")

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use("clam")

        # Base styles
        style.configure(".", background=self.bg_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Helvetica", 10),
        )
        style.configure(
            "Title.TLabel",
            font=("Helvetica", 24, "bold"),
            foreground=self.primary_color,
        )
        style.configure(
            "Subtitle.TLabel", font=("Helvetica", 16), foreground=self.secondary_color
        )
        style.configure(
            "SectionTitle.TLabel",
            font=("Helvetica", 14, "bold"),
            foreground=self.primary_color,
            padding=(0, 10, 0, 5),
        )
        style.configure(
            "Algorithm.TButton",
            font=("Helvetica", 12),
            padding=10,
            foreground="white",
            background=self.button_color,
        )
        style.map(
            "Algorithm.TButton",
            background=[
                ("active", self.button_active),
                ("pressed", self.button_hover),
                ("disabled", "#bdc3c7"),
            ],
        )
        style.configure(
            "Footer.TLabel", font=("Helvetica", 9), foreground=self.text_color
        )

    def load_logo(self, path, size=(100, 80)):
        """Load and resize logo image"""
        try:
            if os.path.exists(path):
                img_path = path
            elif os.path.exists(
                os.path.join("assets", "images", os.path.basename(path))
            ):
                img_path = os.path.join("assets", "images", os.path.basename(path))
            elif os.path.exists(os.path.join("assets", os.path.basename(path))):
                img_path = os.path.join("assets", os.path.basename(path))
            elif os.path.exists(os.path.join("images", os.path.basename(path))):
                img_path = os.path.join("images", os.path.basename(path))
            elif os.path.exists(os.path.join(os.getcwd(), os.path.basename(path))):
                img_path = os.path.join(os.getcwd(), os.path.basename(path))
            else:
                raise FileNotFoundError(f"Image not found: {path}")

            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def create_header(self):
        """Create the header with title, subtitle, and logos"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill="x", pady=(0, 20))

        # Left logo
        left_logo_img = self.load_logo("assets/images/ilia.png", size=(200, 70))
        if left_logo_img:
            self.left_logo_img = (
                left_logo_img  # Keep reference to prevent garbage collection
            )
            left_logo_label = ttk.Label(header_frame, image=left_logo_img)
            left_logo_label.pack(side="left", padx=(0, 20))

        # Title and subtitle
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side="left", expand=True)

        self.title_label = ttk.Label(
            title_frame, text="Visualisateur d'Algorithmes", style="Title.TLabel"
        )
        self.title_label.pack()

        self.subtitle_label = ttk.Label(
            title_frame, text="PL & Algorithmes de Graphes", style="Subtitle.TLabel"
        )
        self.subtitle_label.pack()

        # Right logo
        right_logo_img = self.load_logo("assets/images/fste.png", size=(200, 70))
        if right_logo_img:
            self.right_logo_img = (
                right_logo_img  # Keep reference to prevent garbage collection
            )
            right_logo_label = ttk.Label(header_frame, image=right_logo_img)
            right_logo_label.pack(side="right", padx=(20, 0))

    def create_frames(self):
        """Create all application frames with the new layout"""
        # Menu frame
        self.frames["menu"] = ttk.Frame(self.content_container)

        # Main container for algorithm sections
        sections_frame = ttk.Frame(self.frames["menu"])
        sections_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Programmation Linéaire Section
        pl_frame = ttk.Frame(sections_frame)
        pl_frame.pack(side="left", fill="both", expand=True, padx=10)

        pl_title = ttk.Label(
            pl_frame, text="Programmation Linéaire", style="SectionTitle.TLabel"
        )
        pl_title.pack(anchor="w")

        # PL Algorithms
        pl_algorithms = [
            (
                "Simplex",
                "input_simplex",
                "Méthode de programmation linéaire pour l'optimisation",
            ),
            ("Moindre Coût", "input_moindercout", "Méthode du coût minimal"),
            ("Approximation de Vogel", "input_vogels", "Méthode d'approximation"),
            ("Coin Nord-Ouest", "input_northwest", "Méthode du coin nord-ouest"),
        ]

        for algo, frame, tooltip in pl_algorithms:
            btn = ttk.Button(
                pl_frame,
                text=algo,
                style="Algorithm.TButton",
                command=lambda f=frame: self.show_frame(f),
            )
            btn.pack(fill="x", padx=5, pady=5)
            Tooltip(btn, tooltip)

        # Graph Algorithms Section
        graph_frame = ttk.Frame(sections_frame)
        graph_frame.pack(side="right", fill="both", expand=True, padx=10)

        graph_title = ttk.Label(
            graph_frame, text="Algorithmes de Graphes", style="SectionTitle.TLabel"
        )
        graph_title.pack(anchor="w")

        # Graph Algorithms
        graph_algorithms = [
            ("Welsh-Powell", "input_WelshPowell", "Algorithme de coloration de graphe"),
            ("Kruskal", "input_kruskal", "Algorithme d'arbre couvrant minimal"),
            ("Dijkstra", "input_dijkstra", "Algorithme de plus court chemin"),
            (
                "Bellman-Ford",
                "input_bellmanFord",
                "Plus court chemin avec poids négatifs",
            ),
            ("Ford-Fulkerson", "input_fordFulkerson", "Algorithme de flot maximum"),
        ]

        for algo, frame, tooltip in graph_algorithms:
            btn = ttk.Button(
                graph_frame,
                text=algo,
                style="Algorithm.TButton",
                command=lambda f=frame: self.show_frame(f),
            )
            btn.pack(fill="x", padx=5, pady=5)
            Tooltip(btn, tooltip)

        # Create all algorithm frames
        self.frames["input_dijkstra"] = InputDijkstraPage(self.content_container, self)
        self.frames["input_northwest"] = InputNorthwestPage(
            self.content_container, self
        )
        self.frames["input_simplex"] = InputSimplexPage(self.content_container, self)
        self.frames["input_vogels"] = InputVogelsPage(self.content_container, self)
        self.frames["input_moindercout"] = InputMoinderCoutPage(
            self.content_container, self
        )
        self.frames["input_kruskal"] = InputKruskal(self.content_container, self)
        self.frames["input_WelshPowell"] = InputWelshPowell(
            self.content_container, self
        )
        self.frames["input_fordFulkerson"] = InputFordFulkersonPage(
            self.content_container, self
        )
        self.frames["input_bellmanFord"] = InputBellmanFordPage(
            self.content_container, self
        )
        self.frames["visualisation"] = VisualisationFrame(self.content_container, self)

    def create_footer(self):
        """Create footer with credits"""
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.pack(fill="x", pady=(20, 0))

        # Left aligned supervisor
        supervisor_label = ttk.Label(
            footer_frame,
            text="Encadré par:\n    Prof.Something",
            style="Footer.TLabel",
            justify=tk.LEFT,
        )
        supervisor_label.pack(side="left", padx=10)

        # Right aligned team members
        team_label = ttk.Label(
            footer_frame,
            text="Réalisé par:\n    Salim LAGHRIB\n    Mohammed ELLOUZATI\n    Yassine EL AOUNI",
            style="Footer.TLabel",
            justify=tk.LEFT,
        )
        team_label.pack(side="right", padx=10)

    def show_frame(self, frame_name):
        """Show the selected frame"""
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
            frame.grid_forget()

        # Show the selected frame
        if frame_name == "menu":
            self.frames["menu"].pack(fill="both", expand=True)
        else:
            self.frames[frame_name].pack(fill="both", expand=True)

    def change_frame(self, frame_name, algo_name=None):
        """Change frame and handle special cases"""
        if frame_name in [
            "input_dijkstra",
            "input_northwest",
            "input_simplex",
            "input_vogels",
            "input_moindercout",
            "input_WelshPowell",
            "input_kruskal",
            "input_fordFulkerson",
            "input_bellmanFord",
        ]:
            self.show_frame(frame_name)
        elif frame_name == "menu":
            self.show_frame("menu")
        elif frame_name == "visualisation" and algo_name:
            self.show_visualisation(algo_name)

    def show_visualisation(self, algo_name, data=None):
        """Show visualization in a new window"""
        new_window = tk.Toplevel(self.master)
        new_window.title(f"Visualisation - {algo_name}")
        new_window.geometry("1000x700")

        # Configure grid
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

        # Create and show visualization frame
        visualisation_frame = VisualisationFrame(new_window, self)
        visualisation_frame.grid(row=0, column=0, sticky="nsew")
        visualisation_frame.set_algorithm(algo_name)
        if data:
            visualisation_frame.set_data(data)

    show_visualization = show_visualisation  # Alias for US spelling

    def on_closing(self):
        """Handle window closing with confirmation"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

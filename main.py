import tkinter as tk
from gui.pages.main_window import MainWindow
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
import tkinter as tk
import display.Fenetre as F
class Carte(tk.Frame):
    def __init__(self, width: int, height: int, parent: F.Fenetre):  # La classe Fenetre est bien référencée
        super().__init__(parent, bg="lightblue", width=width, height=height)
        self.pack_propagate(False)  # Empêche le redimensionnement automatique
        self.place(x=10 , y=10)
        
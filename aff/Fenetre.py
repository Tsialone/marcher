import tkinter as tk

class Fenetre(tk.Tk):
    def __init__(self, taille: str, titre: str):
        super().__init__() 
        self.title(titre)
        self.geometry(taille)
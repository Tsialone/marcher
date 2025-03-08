import tkinter as tk
from connection.Connection import Connection  

class Fenetre(tk.Tk):
    def __init__(self, taille: str, titre: str):
        super().__init__()
        self.title(titre)
        self.geometry(taille)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Méthode appelée lors de la fermeture de la fenêtre"""
        print("Fermeture de la fenêtre...")
        Connection.close() 
        self.destroy() 

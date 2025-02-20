import tkinter as tk
from tkinter import ttk
import aff.Fenetre as F
from tsena.Box import *
from  fonction.Ecouteur import *
class Formulaire(tk.Frame):
    def __init__(self, width: int, height: int, parent: F.Fenetre): 
        super().__init__(parent, bg="lightgrey", width=width, height=height)
        self.pack_propagate(False)  
        self.place(x=750 , y=10)
        label = tk.Label(self, text="Formulaire", bg="lightgrey")
        label.pack(pady=20)
        self.component()
        

    def component (self):
        # Première Combobox
        payementAnnee = ttk.Combobox(self, values=[2021, 2022, 2023, 2024, 2025], width=10)
        payementAnnee.place(x=10 , y=50)# Aligner à gauche avec un padding

        # Deuxième Combobox
        mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        payementMois = ttk.Combobox(self, values=mois, width=12)
        payementMois.place(x=100 , y=50)# Aligner à gauche avec un padding

        # Troisième Combobox
        allBox = Box().getAll()
        boxsId = []
        for box in allBox:
            boxsId.append(box.getIdBox())
        payementBox = ttk.Combobox(self, values=boxsId, width=12 )
        payementBox.place(x=200 , y=50)
        
        #payement submit
        self.submit = tk.Button(self, text="Payer", command=Ecouteur.payementBlock , width=10) 
        self.submit.place(x=300 , y=50)
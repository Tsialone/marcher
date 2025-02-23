import tkinter as tk
from tkinter import ttk
import aff.Fenetre as F
from tsena.Box import *
from  fonction.Ecouteur import Ecouteur
class Formulaire(tk.Frame):
    
    def __init__(self, width: int, height: int, parent: F.Fenetre): 
        super().__init__(parent, bg="lightgrey", width=width, height=height)
        self.pack_propagate(False)  
        self.place(x=750 , y=10)
        label = tk.Label(self, text="Formulaire", bg="lightgrey")
        label.pack(pady=20)
        self.Payementcomponent()
        self.verificationComponent()

    def Payementcomponent (self):
        # Première Combobox
        values= []
        for i in range(2030 , 2000 , -1):
            values.append(i)
        self.payementAnnee = ttk.Combobox(self,values= values, width=7)
        self.payementAnnee.place(x=10 , y=50)# Aligner à gauche avec un padding

        # Deuxième Combobox
        mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        
        self.payementMois = ttk.Combobox(self, values=mois, width=7)
        self.payementMois.place(x=80 , y=50)# Aligner à gauche avec un padding

        # Troisième Combobox
        allBox = Box().getAll()
        boxsId = []
        for box in allBox:
            boxsId.append(box.getIdBox())
        self.payementBox = ttk.Combobox(self, values=boxsId, width=7 )
        self.payementBox.place(x=150 , y=50)
        
        self.Payementmontant = ttk.Entry(self, width=15 )
        self.Payementmontant.place(x=220 , y=50)
        self.Payementmontant.insert(0 , "Montant")
        
        #payement submit
        self.submit = tk.Button(self, text="Payer", command=lambda:Ecouteur.payementBlock(self.payementBox , self.payementMois , self.payementAnnee) , width=5) 
        self.submit.place(x=320 , y=50)
    def verificationComponent (self):
        # Première Combobox
        values= []
        for i in range(2030 , 2000 , -1):
            values.append(i)
        self.verificationAnnee = ttk.Combobox(self, values=values, width=10)
        self.verificationAnnee.place(x=10 , y=100)# Aligner à gauche avec un padding

        # Deuxième Combobox
        mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        self.verificationMois = ttk.Combobox(self, values=mois, width=12)
        self.verificationMois.place(x=100 , y=100)# Aligner à gauche avec un padding

        
        #payement submit
        self.submitV = tk.Button(self, text="Check", command=lambda: Ecouteur.verification(self.verificationMois , self.verificationAnnee), width=10) 
        self.submitV.place(x=200 , y=100)
    
    
import tkinter as tk
from tkinter import ttk
import display.Fenetre as F
from tsena.Box import *
from fonction.Ecouteur import Ecouteur
from tsena.Locataire import Locataire

class Formulaire(tk.Frame):
    def __init__(self, width: int, height: int, parent: F.Fenetre):
        super().__init__(parent, bg="lightgrey", width=width, height=height)
        self.pack_propagate(False)
        self.place(x=900, y=10)
        label = tk.Label(self, text="Formulaire", bg="lightgrey")
        label.pack(pady=20)
        self.idLocataireLabel  = []
        self.detteLabel   = []
        
        self.Payementcomponent()
        self.verificationComponent()
        self.contratComponent()

    def Payementcomponent(self):
        mois = [
            "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet",
            "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
        ]
        values = [i for i in range(2030, 2000, -1)]
        
        # Combobox Locataire
        allLocataire = Locataire().getAll()
        locatairesId = [locataire.getIdLocataire() for locataire in allLocataire]
        self.payementLocataire = ttk.Combobox(self, values=locatairesId, width=10)
        self.payementLocataire.place(x=10, y=50)
        if locatairesId:
            self.payementLocataire.insert(0, locatairesId[0])
        #date de mayement
        date_label = tk.Label(self, text="Date de payement", bg="lightgrey")
        date_label.place(x=10, y=75) 
        
        self.date_payementAnnee = ttk.Combobox(self, values=values, width=7)
        self.date_payementAnnee.place(x=10, y=95) 
        now_month  = date.today().month
        now_year = date.today().year
        self.date_payementAnnee.insert(0, now_year)
        
        self.date_payementMois = ttk.Combobox(self, values=mois, width=7)
        self.date_payementMois.place(x=80, y=95)  
        self.date_payementMois.insert(0, Ecouteur.moisMapping_reverse[now_month])
        
        
        
        

        # # Combobox Box
        # allBox = Box().getAll()
        # boxsId = [box.getIdBox() for box in allBox]
        # self.payementBox = ttk.Combobox(self, values=boxsId, width=10)
        # self.payementBox.place(x=100, y=50)  # Rapprochement avec Locataire
        # if boxsId:
        #     self.payementBox.insert(0, boxsId[0])

        # Combobox Année
        self.payementAnnee = ttk.Combobox(self, values=values, width=7)
        self.payementAnnee.place(x=95, y=50)  # Décalage vers la droite
        self.payementAnnee.insert(0, "Annee")

        # Combobox Mois
        self.payementMois = ttk.Combobox(self, values=mois, width=7)
        self.payementMois.place(x=165, y=50)  # Décalage vers la droite
        self.payementMois.insert(0, "Mois")

        # Entry Montant
        self.Payementmontant = ttk.Entry(self, width=15)
        self.Payementmontant.place(x=235, y=50)  # Décalage vers la droite
        self.Payementmontant.insert(0, "Montant")

        # Bouton Payer
        self.submit = tk.Button(
            self,
            text="Payer",
            command=lambda: Ecouteur.payementBlock(
                self.payementLocataire, # Ajout de payementLocataire
                self.payementMois,
                self.payementAnnee,
                self.Payementmontant,
                self.date_payementMois,
                self.date_payementAnnee
            ),
            width=5,
        )
        self.submit.place(x=150, y=95) # Décalage vers la droite

    def verificationComponent(self):
        # Première Combobox
        values = []
        for i in range(2030, 2000, -1):
            values.append(i)
        self.verificationAnnee = ttk.Combobox(self, values=values, width=10)
        self.verificationAnnee.place(x=10, y=200)  # Aligner à gauche avec un padding
        self.verificationAnnee.insert(0, "Annee")

        # Deuxième Combobox
        mois = [
            "Janvier",
            "Fevrier",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Aout",
            "Septembre",
            "Octobre",
            "Novembre",
            "Decembre",
        ]
        self.verificationMois = ttk.Combobox(self, values=mois, width=12)
        self.verificationMois.place(x=100, y=200)  # Aligner à gauche avec un padding
        self.verificationMois.insert(0, "Mois")

        # payement submit
        self.submitV = tk.Button(
            self,
            text="Check",
            command=lambda: Ecouteur.verification(
                self.verificationMois, self.verificationAnnee
            ),
            width=10,
        )
        self.submitV.place(x=200, y=200)

    def contratComponent(self):
        
        mois = [
            "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet",
            "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
        ]
        values = [i for i in range(2030, 2000, -1)]
        
        self.dette_payementAnnee = ttk.Combobox(self, values=values, width=7)
        self.dette_payementAnnee.place(x=10, y=250) 
        now_month  = date.today().month
        now_year = date.today().year
        self.dette_payementAnnee.insert(0, now_year)
        
        self.date_payementMois = ttk.Combobox(self, values=mois, width=7)
        self.date_payementMois.place(x=80, y=250)  
        self.date_payementMois.insert(0, Ecouteur.moisMapping_reverse[now_month])
        # Combobox pour les locataires
        

        # Bouton pour valider
        self.makeContratButton = tk.Button(
            self,
            text="Dette",
            command=lambda: Ecouteur.dette(
                self.date_payementMois , 
                self.dette_payementAnnee,
                self
            ),
            width=8,
        )  

        self.makeContratButton.place(x=150, y=250)
    def textDette(self,  lisDictionnary):
        #colonnes
        self.locataireColonne = tk.Label(self, text="Locataire", bg="lightgrey")
        self.locataireColonne.place(x=10, y=280) 
        
        self.totalDette = tk.Label(self, text="Dette", bg="lightgrey")
        self.totalDette.place(x=300, y=280) 
        
        margin = 300
        self.idLocataireLabel.clear()
        self.detteLabel.clear()
        
        for dico in lisDictionnary: 
            idLocataire = dico["idLocataire"]
            dette = dico["dette"]
            self.idLocataireLabel.append(tk.Label(self, text=idLocataire, bg="lightgrey"))
            self.detteLabel.append(tk.Label(self, text=dette, bg="lightgrey"))
                
                # self.idLocataire = tk.Label(self, text=idLocataire, bg="lightgrey")
                # self.idLocataire.place(x=10, y=margin) 
                # if self.dette:
                #     self.dette.config(text="xxxx")
                # else:
                #     self.dette = tk.Label(self, text=dette, bg="lightgrey")
                # margin += 20
        
        
        
        
        
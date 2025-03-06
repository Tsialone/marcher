import tkinter as tk
from tkinter import ttk
import aff.Fenetre as F
from tsena.Box import *
from fonction.Ecouteur import Ecouteur
from tsena.Locataire import Locataire

class Formulaire(tk.Frame):
    def __init__(self, width: int, height: int, parent: F.Fenetre):
        super().__init__(parent, bg="lightgrey", width=width, height=height)
        self.pack_propagate(False)
        self.place(x=750, y=10)
        label = tk.Label(self, text="Formulaire", bg="lightgrey")
        label.pack(pady=20)
        self.Payementcomponent()
        self.verificationComponent()
        self.contratComponent()

    def Payementcomponent(self):
        # Première Combobox
        values = []
        for i in range(2030, 2000, -1):
            values.append(i)
        self.payementAnnee = ttk.Combobox(self, values=values, width=7)
        self.payementAnnee.place(x=10, y=50)  # Aligner à gauche avec un padding
        self.payementAnnee.insert(0, "Annee")
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
        self.payementMois = ttk.Combobox(self, values=mois, width=7)
        self.payementMois.place(x=80, y=50)
        self.payementMois.insert(0, "Mois")

        # Troisième Combobox
        allBox = Box().getAll()
        boxsId = []
        for box in allBox:
            boxsId.append(box.getIdBox())
        self.payementBox = ttk.Combobox(self, values=boxsId, width=7)
        self.payementBox.place(x=150, y=50)
        self.payementBox.insert(0, "Box")

        self.Payementmontant = ttk.Entry(self, width=15)
        self.Payementmontant.place(x=220, y=50)
        self.Payementmontant.insert(0, "Montant")

        # payement submit
        self.submit = tk.Button(
            self,
            text="Payer",
            command=lambda: Ecouteur.payementBlock(
                self.payementBox,
                self.payementMois,
                self.payementAnnee,
                self.Payementmontant,
            ),
            width=5,
        )
        self.submit.place(x=320, y=50)

    def verificationComponent(self):
        # Première Combobox
        values = []
        for i in range(2030, 2000, -1):
            values.append(i)
        self.verificationAnnee = ttk.Combobox(self, values=values, width=10)
        self.verificationAnnee.place(x=10, y=100)  # Aligner à gauche avec un padding
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
        self.verificationMois.place(x=100, y=100)  # Aligner à gauche avec un padding
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
        self.submitV.place(x=200, y=100)

    def contratComponent(self):
        # Combobox pour les locataires
        tempLocataires = Locataire ()
        locataires = []  
        for loc in tempLocataires.getAll():
            locataires.append(loc.getIdLocataire())
       
        self.contratLocataire = ttk.Combobox(self, values=locataires, width=10)
        self.contratLocataire.place(x=10, y=150)
        if locataires:
            self.contratLocataire.insert(0, locataires[0])

        # Combobox pour les boxes
        allBox = Box().getAll()
        boxsId = [box.getIdBox() for box in allBox]
        self.contratBox = ttk.Combobox(self, values=boxsId, width=7)
        self.contratBox.place(x=100, y=150)
        if boxsId:
            self.contratBox.insert(0, boxsId[0])

        # Entrée pour la date de début (MM-AAAA)
        self.contratDateDebut = ttk.Entry(self, width=10)  # Réduit la largeur
        self.contratDateDebut.place(x=170, y=150)
        self.contratDateDebut.insert(0, "MM-AAAA")

        # Entrée pour la date de fin (MM-AAAA)
        self.contratDateFin = ttk.Entry(self, width=10)  # Réduit la largeur
        self.contratDateFin.place(x=240, y=150)
        self.contratDateFin.insert(0, "MM-AAAA")

        # Bouton pour valider
        # idLocataire , idBox, dateDebut , dateFin
        self.makeContratButton = tk.Button(
            self,
            text="Contrat",
            command=lambda: Ecouteur.makeContrat(
                self.contratLocataire,
                self.contratBox,
                self.contratDateDebut,
                self.contratDateFin,
            ),
            width=8,
        )  # Réduit la largeur

        self.makeContratButton.place(x=310, y=150)

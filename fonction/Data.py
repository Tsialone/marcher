from datetime import date
from aff import Carte
from tsena.Marcher import Marcher
from tsena.MarcherBox import MarcherBox
from tsena.PayementBox import PayementBox
from tsena.Box import Box
from tsena.Contrat import Contrat


class Data:
    
    dateExercice = date(2024 , 1 , 1)
    tempMarcher = Marcher()
    tempBox = Box()
    tempMarcherBox = MarcherBox()
    tempPayementBox = PayementBox()

    allMarcherBox = tempMarcherBox.getAll()
    allPayementBox = tempPayementBox.getAll()
    allBox = tempBox.getAll()
    allMarcher = None
    carte = None
    fenetre = None

    @staticmethod
    def drawMarcher(carte=Carte):
        for marcher in Data.allMarcher:
            marcher.dessinerBox(carte)

    @staticmethod
    def drawProgress(mois , annee):
        for marcher in Data.allMarcher:
            marcher.drawProgBox(mois , annee)

    @staticmethod
    def delete():
        for widget in Data.carte.winfo_children():
            widget.destroy()

    @staticmethod
    def changeColor(mois, annee):
        payement = PayementBox()
        tempContrat = Contrat ()
        for marcher in Data.allMarcher:
            for box in marcher.getBoxs():
                if tempContrat.getContratByIdBox(box.getIdBox(), mois, annee) is None:
                    box.setColor("grey")
                else:
                    box.setColor("red")
        Data.drawMarcher(Data.carte)
        Data.drawProgress(mois ,annee)

from aff import Carte
from tsena.Marcher import Marcher
from tsena.MarcherBox import MarcherBox
from tsena.PayementBox import PayementBox
from tsena.Box import Box


class Data:
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
        for marcher in Data.allMarcher:
            for box in marcher.getBoxs():
                if payement.aPayer(box.getIdBox(), mois, annee):
                    box.setColor("green")
                else:
                    box.setColor("red")
        Data.drawMarcher(Data.carte)
        Data.drawProgress(mois ,annee)

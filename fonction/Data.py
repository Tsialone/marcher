from datetime import date
from display import Carte
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
    def drawMarcher(carte=Carte , mois:int = None , annee:int = None):
        for marcher in Data.allMarcher:
            if marcher.getCanvas():
                marcher.deleteComponent()
            marcher.dessinerBox(carte , mois , annee)
    @staticmethod
    def delete ():
        for marcher in Data.allMarcher:
             if marcher.getCanvas():
                marcher.deleteComponent()

    @staticmethod
    def drawProgress(mois , annee):
        for marcher in Data.allMarcher:
            marcher.drawProgBox(mois , annee)

    @staticmethod
    def delete():
        for widget in Data.carte.winfo_children():
            widget.destroy()
    @staticmethod
    def drawTextMarcher (mois:int=None , annee:int=None):
        for marcher in Data.allMarcher:
                tempContrat = Contrat()
                largeur = marcher.getLargeur()
                hauteur = marcher.getLongueur()
                margin = 5
                x, y = margin, margin
                max_row_height = 0
                boxs = marcher.getBoxs()
                if boxs:
                    for box in boxs:
                        boxContrat = None
                        if mois and annee:
                            boxContrat = tempContrat.getContratByIdBox(box.getIdBox(), mois, annee)

                        boxLargeur = box.getLargeur()
                        boxLongueur = box.getLongueur()

                        if x + boxLargeur + margin > largeur:
                            x = margin
                            y += max_row_height + margin
                            max_row_height = 0

                      

                        # box.set_width (box.getLargeur())
                        # box.set_height (box.getLongueur())
                       
                        # box.set_width (box.getLargeur())
                        # box.set_height (box.getLongueur())

                        centre_x = x + boxLargeur / 2
                        centre_y = y + boxLongueur / 2
                        locId = None
                        if boxContrat:
                            locId = boxContrat.getIdLocataire()
                        marcher.getCanvas().create_text(
                                centre_x, centre_y, text=f"{box.getIdBox()}:{locId} ", font=("Arial", 10)
                        )
                        x += boxLargeur + margin
                        max_row_height = max(max_row_height, boxLongueur)
                        
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
        Data.drawMarcher(Data.carte , mois=mois , annee=annee)
        Data.drawProgress(mois ,annee)
        Data.drawTextMarcher(mois=mois  , annee=annee)

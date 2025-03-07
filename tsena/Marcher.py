from tkinter import messagebox
from connection.Connection import *
from fonction.Mouse import Mouse
from fonction.Fonction import *
from matplotlib.patches import Rectangle
import tkinter as tk
from tsena.MarcherRa import MarcherRa
from tsena.Box import Box
from aff.Echelle import Echelle
from tsena.Contrat import Contrat
# from fonction.Ecouteur import Ecouteur


class Marcher:
    def __init__(
        self,
        canvas=None,
        idMarcher: str = None,
        nomMarcher=None,
        prixLocation=None,
        x=None,
        y=None,
        longeur=None,
        largeur=None,
    ):
        # if x and y and carte:
        # super().__init__(carte , width=largeur , height=longeur , bg="white" , bd=2 , relief="solid")
        # self.place(x=x , y=y)
        self.__idMarcher = idMarcher
        self.__nomMarcher = nomMarcher
        self.__prixLocation = prixLocation
        if longeur:
            self.__longueur = longeur * Echelle.valeur
        if largeur:
            self.__largeur = largeur * Echelle.valeur
        self.__x = x
        self.__y = y
        self.__canvas = canvas
        self.__boxs = []

    def getCanvas(self):
        return self.__canvas

    def getIdMarcher(self):
        return self.__idMarcher

    def setIdMarcher(self, idMarcher: str):
        self.__idMarcher = idMarcher

    def getNomMarcher(self):
        return self.__nomMarcher

    def setNomMarcher(self, nomMarcher: str):
        self.__nomMarcher = nomMarcher

    def getPrixLocation(self, mois: int, annee: int, insertion=True):
        tempMarcherRa = MarcherRa()
        tempMarcherRa = tempMarcherRa.getMarcherRaByDate(
            self.getIdMarcher(), mois=mois, annee=annee
        )
        if tempMarcherRa:
            if insertion:
                messagebox.showinfo(
                    "Success", f"Changement de prix \n" + str(tempMarcherRa.getValeur()) + "Ar"+"\n" + tempMarcherRa.getIdMarcher() + "\n" + str(date(tempMarcherRa.getAnnee() , tempMarcherRa.getMois() , 1)))
            return float(tempMarcherRa.getValeur() / Echelle.valeur)
        return float(self.__prixLocation / Echelle.valeur)

    def getLongueur(self):
        return self.__longueur

    def getLargeur(self):
        return self.__largeur

    def getById(self, idMarcher):
        objet = None
        query = "SELECT * FROM marcher WHERE idMarcher = ?"
        objetSql = Connection.getExecute(query, (idMarcher,))
        if objetSql:
            objet = Marcher(
                idMarcher=objetSql[0][0],
                nomMarcher=objetSql[0][1],
                prixLocation=objetSql[0][2],
                x=objetSql[0][3],
                y=objetSql[0][4],
                longeur=objetSql[0][5],
                largeur=objetSql[0][6],
            )
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT idMarcher FROM marcher"
        objetSql = Connection.getExecute(query)
        for line in objetSql:
            tempObjet = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet

    def getBoxs(self):
        if not self.__boxs:
            allObjet = []
            tempBox = Box()
            query = "SELECT * FROM marcher_box WHERE idMarcher = ?"
            objetSql = Connection.getExecute(query, (self.getIdMarcher(),))
            for line in objetSql:
                tempObjet = tempBox.getById(line[0])
                allObjet.append(tempObjet)
            self.__boxs = allObjet
            return allObjet
        return self.__boxs

    def setBoxs(self, boxs):
        self.__boxs = boxs

    def drawProgBox(self, mois, annee):
        for box in self.getBoxs():
            tempContrat = Contrat()
            tempContrat = tempContrat.getContratByIdBox(idBox=box.getIdBox() , mois=mois ,annee=annee)
            if tempContrat:
                boxSurface = box.getSurface()
                from tsena.PayementBox import PayementBox

                tempPayementBox = PayementBox()
                tokonyAloha = (
                    self.getPrixLocation(mois=mois, annee=annee, insertion=False)
                    * boxSurface
                )
                voalohaBox = tempPayementBox.getPayerByIdLocationIdBox(
                    tempContrat.getIdLocataire() ,idBox=box.getIdBox(), mois=mois, annee=annee
                )
                porcentageVoaloha = voalohaBox / tokonyAloha
                porcentageVoaloha *= 100
                print(
                    "pourcentage voaloha " + str(porcentageVoaloha) + " " + box.getIdBox() + " tokony aloha " + str(tokonyAloha) + " boxsurface " + str(boxSurface)
                )
                boxLargeur = box.getLargeur()
                boxLongueur = box.getLongueur()
                x = box.get_x()
                y = box.get_y()

                progressWidth = float(boxLargeur) * (porcentageVoaloha / 100)

                self.__canvas.create_rectangle(
                    x,
                    y,
                    float(x) + float(progressWidth),
                    float(y) + float(boxLongueur),
                    outline="black",
                    fill="green",
                )
                centre_x = x + boxLargeur / 2
                centre_y = y + boxLongueur / 2
                self.__canvas.create_text(
                    centre_x, centre_y, text=box.getIdBox(), font=("Arial", 10, "bold")
                )

    def dessinerBox(self, carte):
        boxs = self.getBoxs()
        largeur = self.getLargeur()
        hauteur = self.getLongueur()
        margin = 5
        #  # super().__init__(carte , width=largeur , height=longeur , bg="white" , bd=2 , relief="solid")
        #     # self.place(x=x , y=y)
        self.__canvas = tk.Canvas(
            carte,
            width=self.__largeur,
            height=self.__longueur,
            bg="white",
            # relief="solid",
        )
        self.__canvas.place(x=self.__x, y=self.__y)
        # self.__canvas.create_oval (self.__x , self.__y , 300 , 300,fill="white" , outline="black")
        # self.__canvas.bind(
        #     "<Button-1>", lambda event: Mouse.clickGauche(event, marcher=self)
        # )
        if boxs:
            x, y = margin, margin
            max_row_height = 0

            for box in boxs:
                # self.__canvas.bind("<Button-1>"  , lambda event: Mouse.clickGauche(event,box=box))

                boxLargeur = box.getLargeur()
                boxLongueur = box.getLongueur()

                if x + boxLargeur + margin > largeur:
                    x = margin
                    y += max_row_height + margin
                    max_row_height = 0

                if y + boxLongueur + margin > hauteur:
                    self.__canvas.config(height=y + boxLongueur + margin)
                    hauteur = self.__canvas.winfo_height()

                # box.set_width (box.getLargeur())
                # box.set_height (box.getLongueur())

                rect = self.__canvas.create_rectangle(
                    (x, y), x + boxLargeur, y + boxLongueur, outline="black", fill=box.getColor()
                )
                box.set_xy((x, y))
                # box.set_width (box.getLargeur())
                # box.set_height (box.getLongueur())

                centre_x = x + boxLargeur / 2
                centre_y = y + boxLongueur / 2
                self.__canvas.create_text(
                    centre_x, centre_y, text=box.getIdBox(), font=("Arial", 10, "bold")
                )

                x += boxLargeur + margin
                max_row_height = max(max_row_height, boxLongueur)

        centre_x_canvas = largeur / 2
        centre_y_canvas = hauteur / 2
        self.__canvas.create_text(
            centre_x_canvas,
            centre_y_canvas,
            text=self.getIdMarcher(),
            font=("Arial", 10, "bold", "italic"),
        )

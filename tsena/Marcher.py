from connection.Connection import *
from fonction.Fonction import *
from matplotlib.patches import Rectangle
from aff.Carte import *
import tkinter as tk
from tsena.Box import Box



class Marcher(tk.Canvas):
    def __init__ (self , carte:Carte=None ,idMarcher:str=None , nomMarcher=None , prixLocation=None , x=None   , y=None , longeur=None , largeur=None   ):
        if x and y and carte:
            super().__init__(carte , width=largeur , height=longeur , bg="white" , bd=2 , relief="solid")
            self.place(x=x , y=y)
        self.__idMarcher = idMarcher
        self.__nomMarcher = nomMarcher
        self.__prixLocation = prixLocation
        self.__longueur   = longeur
        self.__largeur  = largeur
        self.__boxs = []
    
    def getIdMarcher (self):
        return  self.__idMarcher
    def setIdMarcher (self , idMarcher:str):
        self.__idMarcher = idMarcher
    
    def getNomMarcher (self):
        return self.__nomMarcher
    
    def setNomMarcher  (self , nomMarcher:str):
        self.__nomMarcher = nomMarcher
    
    def getPrixLocation (self):
        return self.__prixLocation
    def getLongueur (self):
        return self.__longueur
    def getLargeur (self):
        return self.__largeur
    
    def getById (self , idMarcher , carte):
        objet = None
        query = "SELECT * FROM marcher WHERE idMarcher = ?"
        objetSql = Connection.getExecute(query, (idMarcher,))
        if objetSql:
            objet = Marcher(carte=carte,idMarcher=objetSql[0][0], nomMarcher=objetSql[0][1],prixLocation= objetSql[0][2] ,x= objetSql[0][3] , y=objetSql[0][4] ,longeur= objetSql[0][5] ,largeur= objetSql[0][6])
        return objet
    def getAll (self , carte:Carte):
        allObjet  = []
        query = "SELECT idMarcher FROM marcher"
        objetSql = Connection.getExecute(query)
        for line in objetSql:
            tempObjet  = self.getById(line[0]  ,carte=carte)
            allObjet.append(tempObjet)
        return allObjet
    def getBoxs (self):
        if not self.__boxs:
            allObjet  = []
            tempBox = Box()
            query = "SELECT * FROM marcher_box WHERE idMarcher = ?"
            objetSql = Connection.getExecute(query , (self.getIdMarcher(),))
            for line in objetSql:
                tempObjet  = tempBox.getById(line[0])
                allObjet.append(tempObjet)
            self.__boxs = allObjet
            return allObjet
        return self.__boxs
    def dessinerBox(self):
        boxs = self.getBoxs()
        largeur = self.getLargeur()
        hauteur = self.getLongueur()
        margin = 5  # Marge entre les boîtes

        if boxs:
            x, y = margin, margin  # Position initiale
            max_row_height = 0  # Hauteur max de la ligne en cours

            for box in boxs:
                boxLargeur = box.getLargeur()
                boxLongueur = box.getLongueur()

                # Vérifier si la boîte dépasse la largeur du canvas
                if x + boxLargeur + margin > largeur:
                    x = margin  # Retour à gauche
                    y += max_row_height + margin  # Descendre d'une ligne
                    max_row_height = 0  # Réinitialiser la hauteur max

                # Vérifier si la boîte dépasse la hauteur du canvas
                if y + boxLongueur + margin > hauteur:
                    self.config(height=y + boxLongueur + margin)  # Augmenter la hauteur du canvas
                    hauteur = self.winfo_height()

                # Dessiner la boîte
                self.create_rectangle(
                    x, y, x + boxLargeur, y + boxLongueur,
                    outline="black", fill=box.getColor()
                )

                # Ajouter l'ID de la boîte au centre de la boîte
                centre_x = x + boxLargeur / 2
                centre_y = y + boxLongueur / 2
                self.create_text(centre_x, centre_y, text=box.getIdBox(), font=("Arial", 10, "bold"))

                # Mise à jour des coordonnées
                x += boxLargeur + margin
                max_row_height = max(max_row_height, boxLongueur)

        # Ajouter la lettre "M" au centre du canvas
        centre_x_canvas = largeur / 2
        centre_y_canvas = hauteur / 2
        self.create_text(centre_x_canvas, centre_y_canvas, text=self.getIdMarcher(), font=("Arial", 10, "bold", "italic"))

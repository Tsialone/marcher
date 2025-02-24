from connection.Connection import *
from datetime import *
from matplotlib.patches import Rectangle
class Box(Rectangle):
    def __init__ (self , idBox=None , nomBox= None  , longeur = None , largeur = None):
        if longeur and largeur:
            super().__init__((0 , 0 ), largeur , longeur)
        self.__idBox  = idBox
        self.__nomBox = nomBox
        self.__longeur  = longeur
        self.__largeur = largeur
        self.__debutExrecice = date(2024 , 1 , 1)
        self.__color = "white"
        
    
    def getIdBox (self):
        return self.__idBox
    def getNomBox(self):
        return self.__nomBox
    def getLongueur (self):
        return self.__longeur
    def getLargeur (self):
        return self.__largeur
    def getDebutExercice(self):
        return self.__debutExrecice
    def getColor (self):
        return self.__color
    def setColor (self , color:str):
        self.__color = color
    
    
    def getById (self , idBox):
        objet = None
        query = "SELECT * FROM box WHERE idBox = ?"
        objetSql = Connection.getExecute(query, (idBox,))
        if objetSql:
            objet = Box(objetSql[0][0], objetSql[0][1], objetSql[0][2] ,objetSql[0][3] )
        return objet
    def getAll (self):
        allObjet  = []
        query = "SELECT idBox FROM box"
        marcheSql = Connection.getExecute(query)
        for line in marcheSql:
            tempObjet  = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet
    def getSurface (self):
        return self.getLargeur() * self.getLongueur()
    
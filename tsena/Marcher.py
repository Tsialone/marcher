from connection.Connection import *
from fonction.Fonction import *

class Marcher:
    def __init__ (self , idMarcher:str=None , nomMarcher=None , prixLocation=None  ):
        self.__idMarcher = idMarcher
        self.__nomMarcher = nomMarcher
        self.__prixLocation = prixLocation
    
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
    def getById (self , idMarcher):
        objet = None
        query = "SELECT * FROM marcher WHERE idMarcher = ?"
        objetSql = Connection.getExecute(query, (idMarcher,))
        if objetSql:
            objet = Marcher(objetSql[0][0], objetSql[0][1], objetSql[0][2])
        return objet
    def getAll (self):
        allObjet  = []
        query = "SELECT idPayement FROM payement_box"
        objetSql = Connection.getExecute(query)
        for line in objetSql:
            tempObjet  = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet
        
        
        
        


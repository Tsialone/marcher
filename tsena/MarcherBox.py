from connection.Connection import *
class MarcherBox:
    def __init__ (self,idBox=None, idMarcher=None):
        self.__idBox  = idBox
        self.__idMarcher = idMarcher
    
    def getIdBox(self):
        return self.__idBox
    def getIdMarcher(self):
        return self.__idMarcher
    
    def getAll (self):
        allObjet  = []
        query = "SELECT * FROM marcher_box"
        objetSql = Connection.getExecute(query)
        if objetSql:
            for line in objetSql:
                tempObjet  =  MarcherBox (line[0] , line[1])
                allObjet.append(tempObjet)
        return allObjet

    
from connection.Connection import Connection
class MarcherRa:
    def __init__(self, idMarcher = None, raison: str=None, pourcentage: float=None, mois: int = None):
        self.__idMarcher = idMarcher
        self.__raison = raison
        self.__pourcentage = pourcentage
        self.__mois = mois

    # Setters
    def set_idMarcher(self, idMarcher):
        self.__idMarcher = idMarcher

    def set_raison(self, raison: str):
        self.__raison = raison

    def set_pourcentage(self, pourcentage: float):
        self.__pourcentage = pourcentage

    def set_mois(self, mois: int):
        self.__mois = mois

    # Getters
    def get_idMarcher(self):
        return self.__idMarcher

    def get_raison(self):
        return self.__raison

    def get_pourcentage(self):
        return self.__pourcentage

    def get_mois(self):
        return self.__mois
    
    def getByIdMarcherMois (self , idMarcher , mois):
        objet = None
        query = "SELECT * FROM marcher_ra WHERE idMarcher = ? and mois = ?"
        objetSql = Connection.getExecute(query, (idMarcher,mois,))
        if objetSql:
            objet = MarcherRa(idMarcher=objetSql[0][0], raison=objetSql[0][1] , pourcentage=objetSql[0][2] , mois=objetSql[0][3])
        return objet
        

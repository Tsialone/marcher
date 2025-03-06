from connection.Connection import Connection
from datetime import *
from fonction.Fonction import Fonction


class MarcherRa:
    def __init__(
        self,
        idMarcherRa=None,
        idMarcher=None,
        annee=None,
        mois: int = None,
        valeur: float = None,
    ):
        self.__idMarcherRa = idMarcherRa
        self.__idMarcher = idMarcher
        self.__annee = annee
        self.__mois = mois
        self.__valeur = valeur

    # Setters
    def setIdMarcherRa(self, idMarcherRa):
        self.__idMarcherRa = idMarcherRa

    def setIdMarcher(self, idMarcher):
        self.__idMarcher = idMarcher

    def setAnnee(self, annee: int):
        self.__annee = annee

    def setMois(self, mois: int):
        self.__mois = mois

    def setValeur(self, valeur: float):
        self.__valeur = valeur

    # Getters
    def getIdMarcherRa(self):
        return self.__idMarcherRa

    def getIdMarcher(self):
        return self.__idMarcher

    def getAnnee(self):
        return self.__annee

    def getMois(self):
        return self.__mois

    def getValeur(self):
        return self.__valeur

    def getById(self, idMarcherRa):
        objet = None
        query = "SELECT * FROM marcher_ra WHERE idMarcherRa = ?"
        objetSql = Connection.getExecute(query, (idMarcherRa,))
        if objetSql:
            objet = MarcherRa(
                objetSql[0][0],
                objetSql[0][1],
                objetSql[0][2],
                objetSql[0][3],
                objetSql[0][4],
            )
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT idMarcherRa FROM marcher_ra"
        objetSql = Connection.getExecute(query)
        for line in objetSql:
            tempObjet = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet

    def getMarcherRaByDate(self, idMarcher, mois, annee):
        allMarcherRa = self.getAll()
        dateAndoavana = date(annee, mois, 1)
        dateTaoAriana = []
        for marcherRa in allMarcherRa:
            # print(marcherRa.getIdMarcher() + " " +  str (date(marcherRa.getAnnee() , marcherRa.getMois() , 1)) + " " +str (marcherRa.getValeur()))
            if marcherRa.getIdMarcher() == idMarcher:
                marcherRaAnnee = marcherRa.getAnnee()
                marcherRaMois = marcherRa.getMois()
                dateFiovana = date(marcherRaAnnee , marcherRaMois , 1)
                # print(dateFiovana)
                if dateFiovana <= dateAndoavana:
                    dateTaoAriana.append(dateFiovana)
        if dateTaoAriana:
            dateTaoArianaTrie = Fonction.trieDate(dateTaoAriana , asc=False)
            for marcherRa in allMarcherRa:
                if marcherRa.getIdMarcher() == idMarcher:
                    marcherRaAnnee = marcherRa.getAnnee()
                    marcherRaMois = marcherRa.getMois()
                    dateFiovana = date(marcherRaAnnee , marcherRaMois , 1)
                    if dateFiovana == dateTaoArianaTrie[0]:
                        # print(str(dateFiovana) + " -> " +  str(dateTaoArianaTrie[0]) + " ->  " + str(marcherRa.getValeur()) )
                        return marcherRa
        return None

# tempMarcherRa = MarcherRa()
# print(tempMarcherRa.getPrixMarcherByDate("Behoririka", 10, 2024))
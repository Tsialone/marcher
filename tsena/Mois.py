from datetime import date
from connection.Connection import Connection


class Mois:
    def __init__(self, valeur, annee, contrat):
        self.__valeur = valeur
        self.__annee = annee
        self.__tokonyAloha = None
        if contrat:
            self.__contrat = contrat

    def getAnnee(self):
        return self.__annee

    def setAnnee(self, annee):
        self.__annee = annee

    def getValeur(self):
        return self.__valeur

    def setValeur(self, valeur):
        self.__valeur = valeur

    def getContrat(self):
        return self.__contrat
    def getTokonyAloha (self):
        return self.__tokonyAloha
    
    def setTokonyAloha(self , tokonyAloha):
        self.__tokonyAloha = tokonyAloha

    def getVoaloha(self):
        somme = 0
        if self.__contrat:
            idLocataire = self.__contrat.getIdLocataire()
            idBox = self.__contrat.getIdBox()
            idContrat = self.__contrat.getIdContrat()
            mois = self.__valeur
            annee = self.__annee
            query = """
            SELECT 
            sum (montant)
            FROM payement_box
            WHERE idLocataire = ? AND idBox = ? AND idContrat = ? AND mois = ? AND annee = ?
        """
            objetSql = Connection.getExecute(
                query, (idLocataire, idBox, idContrat, mois, annee)
            )
            if objetSql and objetSql[0][0]:
                somme = objetSql[0][0]
            else:
                return 0
        return somme

    def tokonyAloha(self, marcher, box):
        if self.__contrat:
            mois = self.__valeur
            annee = self.__annee
            boxSurface = box.getSurface()
            tokonyAloha = (
                marcher.getPrixLocation(mois=mois, annee=annee, insertion=False)
                * boxSurface
            )
            return tokonyAloha
        return None

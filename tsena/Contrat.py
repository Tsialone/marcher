from connection.Connection import *
from datetime import *
from fonction.Fonction import Fonction

class Contrat:
    def __init__(self, idContrat=None, idBox=None, idLocataire=None, moisDebut=None, anneeDebut=None, moisFin=None, anneeFin=None, dateSignature=None):
        self.__idContrat = idContrat
        self.__idBox = idBox
        self.__idLocataire = idLocataire
        self.__moisDebut = moisDebut
        self.__anneeDebut = anneeDebut
        self.__moisFin = moisFin
        self.__anneeFin = anneeFin
        self.__dateSignature = dateSignature

    def getIdContrat(self):
        return self.__idContrat

    def getIdBox(self):
        return self.__idBox

    def getIdLocataire(self):
        return self.__idLocataire

    def getMoisDebut(self):
        return self.__moisDebut

    def getAnneeDebut(self):
        return self.__anneeDebut

    def getMoisFin(self):
        return self.__moisFin

    def getAnneeFin(self):
        return self.__anneeFin

    def getDateSignature(self):
        return self.__dateSignature

    def getById(self, idContrat):
        objet = None
        query = "SELECT * FROM contrat WHERE idContrat = ?"
        objetSql = Connection.getExecute(query, (idContrat,))
        if objetSql:
            objet = Contrat(objetSql[0][0], objetSql[0][1], objetSql[0][2], objetSql[0][3], objetSql[0][4], objetSql[0][5], objetSql[0][6], objetSql[0][7])
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT idContrat FROM contrat"
        contratSql = Connection.getExecute(query)
        for line in contratSql:
            tempObjet = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet

    def insert(self):
        allContrat = self.getAll()
        for contrat in allContrat:
            if contrat.getIdBox() == self.__idBox:  # Vérifier uniquement les contrats pour la même box
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                dateDebut_nouveau = date(self.__anneeDebut, self.__moisDebut, 1)
                dateFin_nouveau = date(self.__anneeFin, self.__moisFin, 1)

                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateDebut_nouveau) or \
                   Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateFin_nouveau) or \
                   Fonction.intersectDate(dateDebut_nouveau, dateFin_nouveau, dateDebut_contrat) or \
                   Fonction.intersectDate(dateDebut_nouveau, dateFin_nouveau, dateFin_contrat):
                    raise ValueError(f"Les dates du contrat chevauchent un contrat existant pour la box {contrat.getIdBox()}\n{contrat.getIdLocataire()}.")

        query = "INSERT INTO contrat (idBox, idLocataire, moisDebut, anneeDebut, moisFin, anneeFin, dateSignature) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (self.__idBox, self.__idLocataire, self.__moisDebut, self.__anneeDebut, self.__moisFin, self.__anneeFin, self.__dateSignature)
        Connection.execute(query, params)

    def update(self):
        query = "UPDATE contrat SET idBox = ?, idLocataire = ?, moisDebut = ?, anneeDebut = ?, moisFin = ?, anneeFin = ?, dateSignature = ? WHERE idContrat = ?"
        params = (self.__idBox, self.__idLocataire, self.__moisDebut, self.__anneeDebut, self.__moisFin, self.__anneeFin, self.__dateSignature, self.__idContrat)
        Connection.execute(query, params)

    def delete(self):
        query = "DELETE FROM contrat WHERE idContrat = ?"
        Connection.execute(query, (self.__idContrat,))
    def getContratByIdBox(self, idBox: str, mois: int, annee: int):
        allContrats = self.getAll()
        dateVerify = date(annee, mois, 1) 

        for contrat in allContrats:
            if contrat.getIdBox() == idBox:
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerify):
                    return contrat  
        return None
            
        

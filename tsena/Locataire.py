from connection.Connection import Connection
from tsena.Contrat import Contrat
from datetime import *
from fonction.Fonction import Fonction
from dateutil.relativedelta import relativedelta
from tsena.Marcher import Marcher
class Locataire:
    def __init__(self, idLocataire=None, nomLocataire=None):
        self.__idLocataire = idLocataire
        self.__nomLocataire = nomLocataire

    def getIdLocataire(self):
        return self.__idLocataire

    def getNomLocataire(self):
        return self.__nomLocataire

    def getById(self, idLocataire):
        objet = None
        query = "SELECT * FROM locataire WHERE idLocataire = ?"
        objetSql = Connection.getExecute(query, (idLocataire,))
        if objetSql:
            objet = Locataire(objetSql[0][0], objetSql[0][1])
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT idLocataire FROM locataire"
        locataireSql = Connection.getExecute(query)
        for line in locataireSql:
            tempObjet = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet

    def insert(self):
        query = "INSERT INTO locataire (idLocataire, nomLocataire) VALUES (?, ?)"
        params = (self.__idLocataire, self.__nomLocataire)
        Connection.getExecute(query, params)

    def update(self):
        query = "UPDATE locataire SET nomLocataire = ? WHERE idLocataire = ?"
        params = (self.__nomLocataire, self.__idLocataire)
        Connection.getExecute(query, params)

    def delete(self):
        query = "DELETE FROM locataire WHERE idLocataire = ?"
        Connection.getExecute(query, (self.__idLocataire,))
    def aBox(self, idBox, mois, annee):
        tempcontrat = Contrat()
        allContrat = tempcontrat.getAll()
        dateVerifie = date(annee, mois, 1)  

        for contrat in allContrat:
            if self.getIdLocataire() == contrat.getIdLocataire() and contrat.getIdBox() == idBox:
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerifie):
                    return True 

        return False  
    
    
    def getDebutExercice(self , idBox , mois:int , annee:int):
        tempcontrat = Contrat()
        allContrat = tempcontrat.getAll()
        dateVerifie = date(annee, mois, 1)  
        for contrat in allContrat:
            if self.getIdLocataire() == contrat.getIdLocataire() and contrat.getIdBox() == idBox:
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerifie):
                    return dateDebut_contrat
        return None
    def getFinExercice(self , idBox , mois:int , annee:int):
        tempcontrat = Contrat()
        allContrat = tempcontrat.getAll()
        dateVerifie = date(annee, mois, 1)  
        for contrat in allContrat:
            if self.getIdLocataire() == contrat.getIdLocataire() and contrat.getIdBox() == idBox:
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerifie):
                    # date_precedente = dateFin_contrat - relativedelta(months=1)
                    return dateFin_contrat
                    # return dateFin_contrat
        return None
    def getAncienContrat (self , idLocataire):
        allContrats = self.getContrats (idLocataire=idLocataire)
        contrats_tries = sorted(allContrats, key=lambda contrat: date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1))
        # for contrat in contrats_tries:
        return contrats_tries
        
    def getContrats (self , idLocataire):
        tempcontrat = Contrat()
        contrats = []
        allContrat = tempcontrat.getAll()
        for contrat in allContrat:
            if idLocataire == contrat.getIdLocataire():
                contrats.append(contrat)
        return contrats
    def getContratByMoisAnnee (self  , idBox , mois , annee):
        dateVerifie = date(annee, mois, 1)
        tempcontrat = Contrat()  
        allContrats = tempcontrat.getAll()
        for contrat in allContrats:
            if contrat.getIdLocataire() == self.getIdLocataire() and contrat.getIdBox () == idBox :
                dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerifie):
                    return contrat
        return None
            
        
# tempLocataire = Locataire()
# anciennements = tempLocataire.getAncienContrat ('Loc1')
# for contrat in anciennements:
#     print(f"{contrat.getIdContrat()   }   {date(contrat.getAnneeDebut() , contrat.getMoisDebut() ,1)}")
        
        
   
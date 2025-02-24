from connection.Connection import *
from datetime import date
from tsena.Box import Box
from tsena.MarcherBox import MarcherBox
from tsena.Marcher import Marcher
class PayementBox:
    def __init__(
        self, idPayement=None, idBox=None, mois=None, annee=None, datePayement=None
    ):
        self.__idPayement = idPayement
        self.__idBox = idBox
        self.__mois = mois
        self.__annee = annee
        self.__datePayement = datePayement

    # Getters
    def getIdPayement(self):
        return self.__idPayement

    def getIdBox(self):
        return self.__idBox

    def getMois(self):
        return self.__mois

    def getAnnee(self):
        return self.__annee

    def getDatePayement(self):
        return self.__datePayement

    # Setters
    def setIdPayement(self, idPayement):
        self.__idPayement = idPayement

    def setIdBox(self, idBox):
        self.__idBox = idBox

    def setMois(self, mois):
        self.__mois = mois

    def setAnnee(self, annee):
        self.__annee = annee

    def setDatePayement(self, datePayement):
        self.__datePayement = datePayement

    def getById(self, idPayement):
        objet = None
        query = "SELECT * FROM payement_box WHERE idPayement = ?"
        objetSql = Connection.getExecute(query, (idPayement,))
        if objetSql:
            objet = PayementBox(objetSql[0][0], objetSql[0][1], objetSql[0][2] , objetSql[0][3] , objetSql[0][4])
        return objet
    def getAll (self):
        allObjet  = []
        query = "SELECT * FROM payement_box"
        objetSql = Connection.getExecute(query)
        if objetSql:
            for line in objetSql:
                tempObjet  =  PayementBox (line[0] , line[1]  , line[2] , line[3] , line[4])
                allObjet.append(tempObjet)
        return allObjet
    
    def insertPayementBox (self,  idBox,mois:int , annee:int , montant):
            self.verificationDate(idBox   , mois   , annee)
            tempBox  = Box()
            tempBox = tempBox.getById(idBox=idBox)
            boxSurface = tempBox.getSurface()
            tempMarcherBox = MarcherBox ()
            allMarcherBox = tempMarcherBox.getAll()
            tempMarcher = Marcher ()
            marcher  = None
            tokonyAloha = 0
            for marcherBox in allMarcherBox:
                if marcherBox.getIdBox() == idBox:
                        marcher = tempMarcher.getById(marcherBox.getIdMarcher())               
            if marcher:
                tokonyAloha =  marcher.getPrixLocation() * boxSurface
                print ("tokony  aloha " + str(tokonyAloha) + " montant " + str(montant))
                if montant < tokonyAloha:
                    raise Exception ("Montant insuffisant vous devez payer \n" + str(round(tokonyAloha,2)) + "Ar")    
                else:
                    query = "INSERT INTO payement_box (idBox  , mois , annee , datePayement , montant)VALUES(?,?,?,now() ,?)"
                    Connection.execute(query , (idBox,mois , annee , tokonyAloha ))
        
    def verificationDate ( self ,idBox  , mois:int , annee:int):
        tempBox =  Box()
        box = tempBox.getById(idBox)
        dateExercice= box.getDebutExercice()
        datePay = date(annee , mois , 1)
        if  dateExercice > datePay:
            raise Exception("Le payement ne doit pas etre avant l'exercice " + str(dateExercice) + " < " + str(date(annee , mois  , 1)) )
    def aPayer ( self ,idBox  , mois:int , annee:int):
        self.verificationDate(idBox=idBox , mois=mois , annee=annee)
        allPayementBox = self.getAll()
        dateAverifie= date(annee , mois , 1)
        for payement in allPayementBox:
            datePaye = date(payement.getAnnee() , payement.getMois() , 1)
            if payement.getIdBox() == idBox and dateAverifie == datePaye:
                return True
        return False
    def getLastPayByBox (self, idBox):
        query = "SELECT * FROM payement_box WHERE idBox = ? ORDER BY DateSerial(annee, mois, 1) DESC"
        objetSql = Connection.getExecute(query , (idBox ,))
        if objetSql:
            for line in objetSql:
                dateTemp = date(line[3] , line[2] , 1)
                return dateTemp
        return None        
    
             
        
    


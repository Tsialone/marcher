from tkinter import messagebox
from connection.Connection import *
from datetime import date
from tsena.Box import Box
from tsena.MarcherBox import MarcherBox
from tsena.Marcher import Marcher
from dateutil.relativedelta import relativedelta
from aff.Echelle import Echelle
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
    
    def insertPayementBox (self,  idBox,mois:int , annee:int , montant:float):
            montant *=  Echelle.valeur
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
                # vola
                tokonyAloha =  0
                voalohaBox =  self.getPayerByIdBox(idBox=idBox , mois=mois , annee=annee)   
                resteApayer = 0
                
                lastPay = self.getLastPayByBox(idBox=idBox)
                debuExo  = tempBox.getDebutExercice()
                jourPay = date(annee , mois , 1)
                
                payer = True
                if lastPay is None:
                        lastPay = debuExo
                if jourPay < lastPay:
                    raise Exception ("Vous avez deja payer cette date:\n" + str(jourPay))
                if jourPay > lastPay:
                    response= messagebox.askquestion ("Confirmation" , "Vous navez pas encore payez la totalite du "+str(lastPay)+"\npayer mantenant?" )
                    if  response =="yes":
                        payer  = True
                    else:
                        payer = False
                        raise Exception ("Payement revoquer")
                if payer:
                    while (montant > 0):
                        mois = lastPay.month
                        annee = lastPay.year
                        tokonyAloha =  marcher.getPrixLocation(mois=mois , annee=annee) * boxSurface
                        voalohaBox =  self.getPayerByIdBox(idBox=idBox , mois=mois , annee=annee)  
                        resteApayer =tokonyAloha - voalohaBox
                        tempMontant = montant - resteApayer
                        if tokonyAloha != voalohaBox:
                            if tempMontant > 0:
                                self.payer (idBox=idBox , mois=  lastPay.month ,annee= lastPay.year , montant=resteApayer)
                                montant -= resteApayer
                            if tempMontant < 0:
                                self.payer (idBox=idBox , mois=  lastPay.month ,annee= lastPay.year , montant=montant)
                                montant = 0
                        if tokonyAloha == voalohaBox:
                            lastPay = lastPay + relativedelta (months=1)

                        
    def payer (self , idBox , mois , annee , montant):
             query = "INSERT INTO payement_box (idBox  , mois , annee  , montant , datePayement)VALUES(?,?,?,?,now())"
             Connection.execute(query , (idBox,mois , annee , montant ))
    def verificationImpayer (self , idBox,mois:int , annee:int , tokonyAloha:float , voaloha:float , montant:float):
        lastPay = self.getLastPayByBox(idBox=idBox)
        jourPay = date(annee , mois , 1)
        # if lastPay == jourPay:
            # raise Exception ("Vous avez deja payez a cette date\n" + str(jourPay))
        if lastPay is None:
            tempBox  = Box ()
            tempBox   = tempBox.getById(idBox=idBox)
            debutExo = tempBox.getDebutExercice()
            if jourPay  == debutExo:
                return debutExo
            response= messagebox.askquestion ("Confirmation" , "Vous navez pas encore payer "+str(debutExo)+" payer mantenant? hahahah" )
            if  response =="yes":
                return debutExo
            else:
                raise Exception ("Veuillez d'abord payer votre location le \n" + str(debutExo))
        elif lastPay and lastPay <= jourPay:
            tempBox  = Box ()
            tempBox   = tempBox.getById(idBox=idBox)
            debutExo = tempBox.getDebutExercice()
            moisPlus1 = lastPay
            resteApayer =tokonyAloha - voaloha 
            montant =montant -resteApayer
            print("Vous avez tout payer il vous reste \n" + str(resteApayer) + " Ar pour" + str(tokonyAloha))
            
            if resteApayer >=0:
                # moisPlus1 = lastPay + relativedelta (months=1)
                response= messagebox.askquestion ("Confirmation" , "Il vous reste a payer "+str(resteApayer)+"Ar pour "+str(jourPay)+" \npayer mantenant?" )
            if  response =="yes":
                self.insertPayementBox(idBox=idBox , mois=mois , annee=annee , montant=montant)
                # return moisPlus1
                # raise Exception ("Vous avez tout payer il vous reste \n" + str(resteApayer) + " Ar pour" + str(tokonyAloha))
            # print(str(moisPlus1) + "  " + str(jourPay))
            if moisPlus1 == jourPay:
                return moisPlus1
            response= messagebox.askquestion ("Confirmation" , "Vous navez pas encore payer "+str(moisPlus1)+" payer mantenant?" )
            if  response =="yes":
                return moisPlus1
            else:
                raise Exception ("Veuillez d'abord payer votre location le \n" + str(moisPlus1))
        
    def verificationDate ( self ,idBox  , mois:int , annee:int):
        tempBox =  Box()
        box = tempBox.getById(idBox)
        from fonction.Data import Data
        dateExercice= Data.dateExercice
        datePay = date(annee , mois , 1)
        if  dateExercice > datePay:
            raise Exception("Le payement ne doit pas etre avant l'exercice " + str(dateExercice) + " < " + str(date(annee , mois  , 1)) )
    def aPayer ( self ,idBox  , mois:int , annee:int):
        self.verificationDate(idBox=idBox , mois=mois , annee=annee)
        tempBox = Box ()
        tempBox = tempBox.getById(idBox)
        tempMarcherBox = MarcherBox ()
        
        allMarcherBox = tempMarcherBox.getAll()
        tempMarcher = Marcher ()
        marcher  = None
        
        boxSurface = tempBox.getSurface ()
        for marcherBox in allMarcherBox:
            if marcherBox.getIdBox() == idBox:
                    marcher = tempMarcher.getById(marcherBox.getIdMarcher())     
                    break          
        if marcher:
            tokonyAloha = marcher.getPrixLocation(mois=mois , annee=annee , insertion=False) * boxSurface
            voalohaBox =  self.getPayerByIdBox(idBox=idBox , mois=mois , annee=annee)
            if tokonyAloha == voalohaBox:
                return True
        
        return False
       
    def getLastPayByBox (self, idBox):
        query = "SELECT * FROM payement_box WHERE idBox = ? ORDER BY DateSerial(annee, mois, 1) DESC"
        tempBox = Box()
        tempBox = tempBox.getById(idBox=idBox)
        objetSql = Connection.getExecute(query , (idBox ,))
        if objetSql:
            for line in objetSql:
                dateTemp = date(line[3] , line[2] , 1)
                return dateTemp
        return None
    def getPayerByIdBox (self , idBox , mois:int , annee:int):
        somme = 0
        query = "SELECT * FROM payement_box WHERE idBox = ? AND mois = ? AND annee = ?"
        tempBox = Box()
        tempBox = tempBox.getById(idBox=idBox)
        objetSql = Connection.getExecute(query , (idBox , mois , annee,))
        if objetSql:
            for line in objetSql:
                somme += line[4]
        return float (somme)
        
    
                           
                                
                        
        
        
    
             
        
    


from tkinter import messagebox
from connection.Connection import *
from datetime import date
from tsena.Box import Box
from tsena.MarcherBox import MarcherBox
from tsena.Marcher import Marcher
from dateutil.relativedelta import relativedelta
from aff.Echelle import Echelle
from tsena.Locataire import Locataire
from tsena.Contrat import Contrat
from fonction.Fonction import Fonction
class PayementBox:
    def __init__(
        self, idPayement=None,idLocataire = None ,  idBox=None,  mois=None, annee=None,montant=None , datePayement=None
    ):
        self.__idPayement = idPayement
        self.__idLocataire  = idLocataire
        self.__idBox = idBox
        self.__mois = mois
        self.__annee = annee
        self.__montant = montant
        self.__datePayement = datePayement

    # Getters
    def getIdPayement(self):
        return self.__idPayement
    def getIdLocataire(self):
        return self.__idLocataire
    
    def getMontant (self):
        return self.__montant

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
            objet = PayementBox(objetSql[0][0], objetSql[0][1], objetSql[0][2] , objetSql[0][3] , objetSql[0][4] , objetSql[0][5] , objetSql[0][6])
        return objet
    def getAll (self):
        allObjet  = []
        query = "SELECT * FROM payement_box"
        objetSql = Connection.getExecute(query)
        if objetSql:
            for line in objetSql:
                tempObjet  =  PayementBox (line[0] , line[1]  , line[2] , line[3] , line[4] , line[5] , line[6])
                allObjet.append(tempObjet)
        return allObjet
    
    def insertPayementBox (self, idLocataire , idBox,mois:int , annee:int , montant:float):
            montant *=  Echelle.valeur
            tempLocataire = Locataire ()
            tempLocataire  = tempLocataire.getById(idLocataire=idLocataire)
            locataireContrat = tempLocataire.getContratByMoisAnnee(idBox=idBox, mois=mois  ,annee=annee)
            allSortedContrat = tempLocataire.getAncienContrat(tempLocataire.getIdLocataire())
            if tempLocataire.aBox (idBox=idBox , mois=mois , annee=annee) is not True:
                raise Exception (f"Vous n'avez pas louez cette box:{idBox} veuillez choir une autre")
            self.verificationDate(idBox   , mois   , annee , idLocataire=idLocataire)
            tempBox  = Box()
            tempBox = tempBox.getById(idBox=idBox)
            boxSurface = tempBox.getSurface()
            tempMarcherBox = MarcherBox ()
            allMarcherBox = tempMarcherBox.getAll()
            tempMarcher = Marcher ()
            marcher  = None
            tokonyAloha = 0
            
            for contrat in allSortedContrat:
                if self.aPayer (idLocataire=idLocataire  , idBox=idBox , mois=mois , annee=annee  ,  contrat=  locataireContrat) is not True and contrat.getIdBox() != idBox:
                    response= messagebox.askquestion ("Confirmation" , "Vous devez payer votre box"+str(contrat.getIdBox())+"\npayer mantenant?" )
                    if  response =="yes":
                        payer  = True
                        idBox = contrat.getIdBox()
                        break
                    else:
                        payer = False
                        raise Exception ("Payement revoquer")
                
            for marcherBox in allMarcherBox:
                if marcherBox.getIdBox() == idBox:
                        marcher = tempMarcher.getById(marcherBox.getIdMarcher())               
            if marcher:
            #     # vola
                tokonyAloha =  0
                voalohaBox =  self.getPayerByIdLocationIdBox( idLocataire=idLocataire,idBox=idBox ,  contrat=locataireContrat)   
                resteApayer = 0
                
                lastPay = self.getLastPayByLocataireBox(idLocataire=idLocataire,idBox=idBox)
                debuExo  = tempLocataire.getDebutExercice(idBox=idBox , mois=mois , annee=annee)
                jourPay = date(annee , mois , 1)
                
                payer = True
                if lastPay is None:
                    lastPay = debuExo
                if jourPay < lastPay:
                    raise Exception ("Vous avez deja payer cette date:\n" + str(jourPay))
                if jourPay > lastPay:
                    response= messagebox.askquestion ("Confirmation" , "Vous navez pas encore payez la totalite du "+str(lastPay)+"\npayer mantenant? xxxx" )
                    if  response =="yes":
                        payer  = True
                    else:
                        payer = False
                        raise Exception ("Payement revoquer")
                # if allSortedContrat:
                    # for contrat in allSortedContrat:
                        # if self.aPayer (contrat.getIdLocataire() , contrat.getIdBox() , contrat.get)
                    
                if payer:
                    print(f"last pay{lastPay} {tempLocataire.getFinExercice(idBox=idBox , mois=mois , annee=annee)} {tempLocataire.getIdLocataire()}")
                    while (montant > 0 and tempLocataire.getFinExercice(idBox=idBox , mois=mois , annee=annee) and lastPay <= tempLocataire.getFinExercice(idBox=idBox , mois=mois , annee=annee)):
                        mois = lastPay.month
                        annee = lastPay.year
                        tokonyAloha =  marcher.getPrixLocation(mois=mois , annee=annee) * boxSurface
                        voalohaBox = float  (self.getPayerByIdLocationIdBox( idLocataire=idLocataire,idBox=idBox , contrat= locataireContrat)   )
                        
                        # if lastPay >= tempLocataire.getFinExercice(idBox=idBox , mois=mois , annee=annee) :
                            # raise Exception (f"Vous avez tout payer tokony{tokonyAloha }  voaloha  {voalohaBox}")
                        resteApayer =tokonyAloha - voalohaBox
                        tempMontant = montant - resteApayer
                        if tokonyAloha != voalohaBox:
                            if tempMontant > 0:
                                self.payer (idLocataire=idLocataire ,idBox=idBox , mois=  lastPay.month ,annee= lastPay.year , montant=resteApayer)
                                montant -= resteApayer
                            if tempMontant < 0:
                                self.payer (idLocataire=idLocataire , idBox=idBox , mois=  lastPay.month ,annee= lastPay.year , montant=montant)
                                montant = 0
                        if tokonyAloha == voalohaBox:
                            lastPay = lastPay + relativedelta (months=1)
                        

                        
    def payer(self, idLocataire, idBox, mois, annee, montant):
        query = """
            INSERT INTO payement_box (idLocataire, idBox, mois, annee, montant, datePayement)
            VALUES (?, ?, ?, ?, ?, Now())
        """
        params = (idLocataire, idBox, mois, annee, montant)
        Connection.execute(query, params)
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
        
    def verificationDate ( self ,idBox  , mois:int , annee:int , idLocataire =None):
        if idLocataire:
            tempLocataire = Locataire ()
            datePay = date(annee , mois , 1)
            tempLocataire  = tempLocataire.getById(idLocataire=idLocataire)
            debutExo = tempLocataire.getDebutExercice(idBox=idBox , mois=mois , annee=annee)
            if  debutExo and debutExo > datePay:
                raise Exception("Le payement ne doit pas etre avant l'exercice " + str(debutExo) + " < " + str(date(annee , mois  , 1)) )
        else:
            tempBox =  Box()
            box = tempBox.getById(idBox)
            from fonction.Data import Data
            dateExercice= Data.dateExercice
            datePay = date(annee , mois , 1)
            if  dateExercice > datePay:
                raise Exception("Le payement ne doit pas etre avant l'exercice " + str(dateExercice) + " < " + str(date(annee , mois  , 1)) )
    def aPayer ( self ,idLocataire , idBox  , mois  , annee  , contrat ):
        self.verificationDate(idBox=idBox , mois=mois , annee=annee , idLocataire=idLocataire)
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
            voalohaBox =  self.getPayerByIdLocationIdBox(idLocataire=idLocataire ,idBox=idBox , contrat=contrat)
            print(f"{tokonyAloha}  {voalohaBox}")
            if tokonyAloha == voalohaBox:
                return True
        return False
       
    def getLastPayByLocataireBox(self, idLocataire, idBox):
        query = """
            SELECT annee, mois
            FROM payement_box
            WHERE idLocataire = ? AND idBox = ?
            ORDER BY annee DESC, mois DESC
        """
        objetSql = Connection.getExecute(query, (idLocataire, idBox))

        if objetSql:
            annee = objetSql[0][0]  # Première ligne, colonne année
            mois = objetSql[0][1]   # Première ligne, colonne mois
            return date(annee, mois, 1)
        else:
            return None
    def getPayerByIdLocationIdBox(self, idLocataire, idBox, contrat):
        somme = 0
        tempPayement = PayementBox()
        allPayement = tempPayement.getAll()

        if contrat:  
            dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
            dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)

            for paye in allPayement:
                if paye.getIdLocataire() == idLocataire and paye.getIdBox() == idBox:
                    dateVerifie = date(paye.getAnnee(), paye.getMois(), 1)
                    if Fonction.intersectDate(dateDebut_contrat, dateFin_contrat, dateVerifie):
                        somme += paye.getMontant()  # Assurez-vous que getMontant() existe

        return somme
        
                                
                        
        
        
    
             
        
    


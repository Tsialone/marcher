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
        self, idPayement=None,idLocataire = None ,  idBox=None, idContrat=None , mois=None, annee=None,montant=None , datePayement=None
    ):
        self.__idPayement = idPayement
        self.__idLocataire  = idLocataire
        self.__idBox = idBox
        self.__idContrat = idContrat
        self.__mois = mois
        self.__annee = annee
        self.__montant = montant
        self.__datePayement = datePayement

    # Getters
    def getIdPayement(self):
        return self.__idPayement
    def getIdLocataire(self):
        return self.__idLocataire
    def getIdContrat(self):
        return self.__idContrat
    
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
    
    def insertPayementBox (self, idLocataire , idBox,mois:int , annee:int , montant:float ):
            montant *=  Echelle.valeur
            print(f"momo {montant}")
            tempLocataire = Locataire ()
            tempLocataire  = tempLocataire.getById(idLocataire=idLocataire)
           
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
            
            locataireContrat = tempLocataire.getContratByMoisAnnee(idBox=idBox, mois=mois  ,annee=annee)
            allSortedContrat = tempLocataire.getAncienContrat(tempLocataire.getIdLocataire())
            
            
            for contrat in allSortedContrat:
                # print(f" {contrat.getIdContrat()} {contrat.getIdBox()} {contrat.getIdLocataire()} {date(contrat.getAnneeDebut() , contrat.getMoisDebut() , 1)} {date(contrat.getAnneeFin() , contrat.getMoisFin() , 1)}" )
                if   contrat.getIdBox() == idBox:
                    print(f"aa miala {idBox}")
                    break
                if self.aPayer (idLocataire=idLocataire  , idBox=contrat.getIdBox() , mois=mois , annee=annee  ,  contrat=  contrat) is not True:
                    response= messagebox.askquestion ("Confirmation" , f"Vous devez payer votre box d'abord {contrat.getIdBox()} \ncontrat:  {date(contrat.getAnneeDebut() , contrat.getMoisDebut() , 1)} - {date(contrat.getAnneeFin() , contrat.getMoisFin() , 1)} \npayer mantenant?" )
                    if  response =="yes":
                        payer  = True
                        idBox = contrat.getIdBox()
                        tempBox = tempBox.getById(idBox=idBox)
                        boxSurface = tempBox.getSurface()
                        locataireContrat = contrat
                        lastPay = self.getLastPayByLocataireBox(idLocataire=idLocataire,idBox=idBox  , idContrat= locataireContrat.getIdContrat() )
                        mois = locataireContrat.getMoisDebut()
                        annee = locataireContrat.getAnneeDebut()
                        if lastPay:
                            mois = lastPay.month
                            annee = lastPay.year
                        break
                    else:
                        payer = False
                        raise Exception ("Payement revoquer")
                
            for marcherBox in allMarcherBox:
                if marcherBox.getIdBox() == idBox:
                        marcher = tempMarcher.getById(marcherBox.getIdMarcher())
                        break               
            if locataireContrat:
                # print(f"contrat any t@ io date io =>{locataireContrat.getIdContrat()} {locataireContrat.getIdBox()} {locataireContrat.getIdLocataire()} {date(locataireContrat.getAnneeDebut() , locataireContrat.getMoisDebut() , 1)} {date(locataireContrat.getAnneeFin() , locataireContrat.getMoisFin() , 1)}")
                # print(f"mois{mois} et anne{annee}")
                tokonyAloha =  marcher.getPrixLocation(mois=mois , annee=annee , insertion=False) * boxSurface
                voalohaBox = float  (self.getPayerByIdLocationIdBox( idLocataire=idLocataire,idBox=idBox , contrat= locataireContrat)   )
                # print(f"tokony aloha {tokonyAloha },  voaloha {voalohaBox}")
            else:
                raise Exception (f"Vous n'avez pas louez cette box {idBox} ou fin de contrat pour {tempLocataire.getFinContrat(idBox=idBox , mois=mois , annee=annee)} {tempLocataire.getIdLocataire()}")
            if marcher:
                #vola
                tokonyAloha =  marcher.getPrixLocation(mois=mois , annee=annee , insertion=False) * boxSurface
                voalohaBox =  self.getPayerByIdLocationIdBox( idLocataire=idLocataire,idBox=idBox ,  contrat=locataireContrat)   
                resteApayer = 0
                
                lastPay = self.getLastPayByLocataireBox(idLocataire=idLocataire,idBox=idBox  , idContrat= locataireContrat.getIdContrat() )
                debuExo  = tempLocataire.getDebutContrat(idBox=idBox , mois=mois , annee=annee)
                jourPay = date(annee , mois , 1)
                print(f"jour pay {jourPay} last pay {debuExo}")
                
                payer = True
                # print(f"last pay {lastPay}")
                if lastPay is None:
                    lastPay = debuExo
                # print(f"last pay after ver {lastPay}")
                
                if   voalohaBox == tokonyAloha:
                    raise Exception ("Vous avez deja payer la totalite cette date:\n" + str(jourPay))
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
                    # print(f"none ? {tempLocataire.getFinContrat(idBox=idBox , mois=staticMois , annee=staticAnnee)}  idBox:{idBox}  mois:{mois} annee:{annee}")
                    while (montant > 0  ):
                        # print(f"last pay{lastPay} {tempLocataire.getFinContrat(idBox=idBox , mois=mois , annee=annee)} {tempLocataire.getIdLocataire()}")
                        mois = lastPay.month
                        annee = lastPay.year
                        tokonyAloha =  marcher.getPrixLocation(mois=mois , annee=annee) * boxSurface
                        voalohaBox = float  (self.getPayerByIdLocationIdBox( idLocataire=idLocataire,idBox=idBox , contrat= locataireContrat)   )
                        
                        # if lastPay >= tempLocataire.getFinExercice(idBox=idBox , mois=mois , annee=annee) :
                            # raise Exception (f"Vous avez tout payer tokony{tokonyAloha }  voaloha  {voalohaBox}")
                        resteApayer =tokonyAloha - voalohaBox
                        tempMontant = montant - resteApayer
                        print(f"reste a payer {resteApayer} tempMontant {tempMontant}")
                        if tokonyAloha != voalohaBox:
                            if tempMontant > 0:
                                self.payer (idLocataire=idLocataire ,idBox=idBox , idContrat=locataireContrat.getIdContrat()  , mois=  lastPay.month ,annee= lastPay.year , montant=resteApayer)
                                montant -= resteApayer
                            if tempMontant <= 0:
                                self.payer (idLocataire=idLocataire ,  idBox=idBox , idContrat=locataireContrat.getIdContrat() , mois=  lastPay.month ,annee= lastPay.year , montant=montant)
                                montant = 0
                                print(f"tss miala eto {montant} {idBox} tokony {tokonyAloha}")
                        if tokonyAloha == voalohaBox:
                            # lastPay = lastPay + relativedelta (months=1)
                            print(f"voaloha daholo {idBox}  mois:{mois} annee:{annee}")
                            tsyMisyAntitra = True
                            for contrat in allSortedContrat:
                                # if   contrat.getIdBox() == idBox:
                                #     print(f"tayy")
                                #     break
                                if  self.aPayer (idLocataire=idLocataire  , idBox=contrat.getIdBox() , mois=mois , annee=annee  ,  contrat=  contrat) is not True:
                                    tsyMisyAntitra = False
                                    print(f"{contrat.getIdBox()}  {contrat.getIdContrat()}")
                                    response= messagebox.askquestion ("Confirmation" , f"Vous devez payer votre box d'abord {contrat.getIdBox()} \ncontrat:  {date(contrat.getAnneeDebut() , contrat.getMoisDebut() , 1)} - {date(contrat.getAnneeFin() , contrat.getMoisFin() , 1)} \npayer mantenant? Recurcive" )
                                    if  response =="yes":
                                        # idBox = contrat.getIdBox()
                                        # mois = contrat.getMoisDebut()
                                        # annee = contrat.getAnneeDebut()
                                        # if lastPay:
                                        #     mois = lastPay.month
                                        #     annee = lastPay.year
                                        print(f"handoa vao2 mois: {contrat.getMoisDebut()} et annee: {contrat.getAnneeDebut()} idBox: {contrat.getIdBox()}")
                                        montant =  self.insertPayementBox (idLocataire , contrat.getIdBox(),contrat.getMoisDebut() , contrat.getAnneeDebut() , montant=montant )
                                        break
                                    else:
                                        raise Exception ("Payement revoquer")
                                if tsyMisyAntitra:
                                    return montant
                    return montant        # print(f" zao ilay none? {lastPay}  hum {date (locataireContrat.getAnneeFin () ,locataireContrat.getMoisFin () , 1)}")
                        

                        
    def payer(self, idLocataire, idBox, idContrat , mois, annee, montant ):
        query = """
            INSERT INTO payement_box (idLocataire, idBox, idContrat , mois, annee, montant, datePayement)
            VALUES (?, ?,?  ,?, ?, ?, Now())
        """
        params = (idLocataire, idBox , idContrat, mois, annee, montant)
        Connection.execute(query, params)
      
    def verificationDate ( self ,idBox  , mois:int , annee:int , idLocataire =None):
        if idLocataire:
            tempLocataire = Locataire ()
            datePay = date(annee , mois , 1)
            tempLocataire  = tempLocataire.getById(idLocataire=idLocataire)
            debutExo = tempLocataire.getDebutContrat(idBox=idBox , mois=mois , annee=annee)
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
            print(f" a verifier {tokonyAloha}  {voalohaBox}")
            if tokonyAloha == voalohaBox:
                return True
                
        return False
       
    def getLastPayByLocataireBox(self, idLocataire, idBox , idContrat):
        query = """
            SELECT annee, mois
            FROM payement_box
            WHERE idLocataire = ? AND idBox = ? AND idContrat = ?
            ORDER BY annee DESC, mois DESC
        """
        objetSql = Connection.getExecute(query, (idLocataire, idBox , idContrat))

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
            for paye in allPayement:
                # print (f"Base {paye.getIdLocataire()} {paye.getIdBox()} { paye.getIdContrat()} ") 
                # print (f"Input {idLocataire} {idBox} { contrat.getIdContrat()} ") 
                
                if paye.getIdLocataire() == idLocataire and paye.getIdBox() == idBox and paye.getIdContrat() == contrat.getIdContrat():
                        # print(f"reto valeur {paye.getMontant()}")
                        somme += paye.getMontant()  
        return somme
        
                            
                                  
             
        
    


from tkinter import messagebox
from connection.Connection import *
from datetime import date
from tsena.Box import Box
from tsena.Contrat import Contrat
from tsena.MarcherBox import MarcherBox
from dateutil.relativedelta import relativedelta
from display.Echelle import Echelle
from tsena.Locataire import Locataire
from tsena.Marcher import Marcher
from decimal import Decimal, getcontext

getcontext().prec = 10


class PayementBox:
    def __init__(
        self,
        idPayement=None,
        idLocataire=None,
        idBox=None,
        idContrat=None,
        mois=None,
        annee=None,
        montant=None,
        datePayement=None,
    ):
        self.__idPayement = idPayement
        self.__idLocataire = idLocataire
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

    def getMontant(self):
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
            objet = PayementBox(
                objetSql[0][0],
                objetSql[0][1],
                objetSql[0][2],
                objetSql[0][3],
                objetSql[0][4],
                objetSql[0][5],
                objetSql[0][6],
            )
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT * FROM payement_box"
        objetSql = Connection.getExecute(query)
        if objetSql:
            for line in objetSql:
                tempObjet = PayementBox(
                    line[0], line[1], line[2], line[3], line[4], line[5], line[6]
                )
                allObjet.append(tempObjet)
        return allObjet

 
    def insertPayementBox(
        self,
        idLocataire,
        mois: int,
        annee: int,
        montant,
        payementMois: int,
        payementAnnee: int,
    ):
        print(f"Miantso *** mois: {mois} annee: {annee} idLocataire: {idLocataire}")

        tempLocataire = Locataire().getById(idLocataire=idLocataire)
        allSortedContrat = tempLocataire.getAncienContrat()

        box_dict = {box.getIdBox(): box for box in Box().getAll()}
        marcherBox_list = MarcherBox().getAll()
        marcherBox_dict = {mb.getIdBox(): mb for mb in marcherBox_list}
        marcher_dict = {}
        for contrat in allSortedContrat:
            box_id = contrat.getIdBox()
            marcherBox = marcherBox_dict.get(box_id)

            if marcherBox:
                marcher_id = marcherBox.getIdMarcher()
                if marcher_id not in marcher_dict:
                    marcher_dict[marcher_id] = Marcher().getById(marcher_id)
                marcher = marcher_dict[marcher_id]

                contratBox = box_dict.get(box_id)
                contrat.initMois(marcher, contratBox)

        # Trouver le premier mois à payer
        moisApayer = self.findMoisApayer(allSortedContrat)

        if not moisApayer:
            print("Aucun mois à payer trouvé.")
            return

        self.processPayment(
            idLocataire,
            moisApayer,
            montant,
            payementMois,
            payementAnnee,
            allSortedContrat
        )

    def findMoisApayer(self, allSortedContrat):
        moisApayer = None
        for contrat in allSortedContrat:
            for mois in contrat.getMois():
                voaloha = Decimal(mois.getVoaloha())
                tokonyAloha = Decimal(mois.getTokonyAloha())

                if voaloha < tokonyAloha:
                    if not moisApayer:
                        moisApayer = mois
                    else:
                        date_current = date(mois.getAnnee(), mois.getValeur(), 1)
                        date_selected = date(moisApayer.getAnnee(), moisApayer.getValeur(), 1)
                        if date_current < date_selected:
                            moisApayer = mois
        return moisApayer

    def processPayment(self, idLocataire, moisApayer, montant, payementMois, payementAnnee, allSortedContrat):
        hisContrat = moisApayer.getContrat()

        print(
            f"**debug Payer {moisApayer.getValeur()}/{moisApayer.getAnnee()} "
            f"tokonyAloha: {moisApayer.getTokonyAloha()} "
            f"voaloha: {moisApayer.getVoaloha()} montant: {montant}"
        )

        dejaPaye = Decimal(moisApayer.getVoaloha())
        aPayer = Decimal(moisApayer.getTokonyAloha()) - dejaPaye

        reste = Decimal(montant) - aPayer

        # Cas 1 : Montant pile ce qu'il faut
        if reste == 0:
            self.payer(
                idLocataire,
                hisContrat.getIdBox(),
                hisContrat.getIdContrat(),
                moisApayer.getValeur(),
                moisApayer.getAnnee(),
                montant,
                payementMois,
                payementAnnee,
            )
            return

        # Cas 2 : Trop payé, il reste de l'argent
        if reste > 0:
            self.payer(
                idLocataire,
                hisContrat.getIdBox(),
                hisContrat.getIdContrat(),
                moisApayer.getValeur(),
                moisApayer.getAnnee(),
                float(montant) - float(reste),
                payementMois,
                payementAnnee,
            )
            print(f"Reste: {reste}, appel récursif insertPayementBox...")
            self.insertPayementBox(
                idLocataire,
                moisApayer.getValeur(),
                moisApayer.getAnnee(),
                float(reste),
                payementMois,
                payementAnnee,
            )
            return

        # Cas 3 : Pas assez, il reste encore à payer
        if reste < 0:
            self.payer(
                idLocataire,
                hisContrat.getIdBox(),
                hisContrat.getIdContrat(),
                moisApayer.getValeur(),
                moisApayer.getAnnee(),
                montant,
                payementMois,
                payementAnnee,
            )
            return
    def payer(
        self,
        idLocataire,
        idBox,
        idContrat,
        mois,
        annee,
        montant,
        payementMois,
        payementAnnee,
    ):
        datePayement = date(payementAnnee, payementMois, 1)
        query = """
            INSERT INTO payement_box (idLocataire, idBox, idContrat , mois, annee, montant, datePayement)
            VALUES (?, ?,?  ,?, ?, ?, ? )
        """
        params = (idLocataire, idBox, idContrat, mois, annee, montant, datePayement)
        Connection.execute(query, params)

    def verificationDate(self, idBox, mois: int, annee: int, idLocataire=None):
        if idLocataire:
            tempLocataire = Locataire()
            datePay = date(annee, mois, 1)
            tempLocataire = tempLocataire.getById(idLocataire=idLocataire)
            debutExo = tempLocataire.getDebutContrat(
                idBox=idBox, mois=mois, annee=annee
            )
            if debutExo and debutExo > datePay:
                raise Exception(
                    "Le payement ne doit pas etre avant l'exercice "
                    + str(debutExo)
                    + " < "
                    + str(date(annee, mois, 1))
                )
        else:
            tempBox = Box()
            box = tempBox.getById(idBox)
            from fonction.Data import Data

            dateExercice = Data.dateExercice
            datePay = date(annee, mois, 1)
            if dateExercice > datePay:
                raise Exception(
                    "Le payement ne doit pas etre avant l'exercice "
                    + str(dateExercice)
                    + " < "
                    + str(date(annee, mois, 1))
                )

    def getLastPayByLocataireBox(self, idLocataire, idBox, idContrat):
        query = """
            SELECT annee, mois
            FROM payement_box
            WHERE idLocataire = ? AND idBox = ? AND idContrat = ?
            ORDER BY annee DESC, mois DESC
        """
        objetSql = Connection.getExecute(query, (idLocataire, idBox, idContrat))

        if objetSql:
            annee = objetSql[0][0]  # Première ligne, colonne année
            mois = objetSql[0][1]  # Première ligne, colonne mois
            return date(annee, mois, 1)
        else:
            return None

    def getLastPayementByContrat(self, idContrat):

        query = """
            SELECT 
            idPayement
            FROM payement_box
            WHERE  idContrat = ?
            ORDER BY annee DESC, mois DESC
        """
        objetSql = Connection.getExecute(query, (idContrat,))

        if objetSql:
            return self.getById(objetSql[0][0])
        else:
            return None

    def getPayerByIdLocationIdBox(self, idLocataire, idBox, idContrat, mois, annee):
        somme = 0
        tempPayement = PayementBox()
        allPayement = tempPayement.getAll()

        for paye in allPayement:
            # print (f"Base {paye.getIdLocataire()} {paye.getIdBox()} { paye.getIdContrat()} ")
            # print (f"Input {idLocataire} {idBox} { contrat.getIdContrat()} ")
            if (
                paye.getIdLocataire() == idLocataire
                and paye.getIdBox() == idBox
                and paye.getIdContrat() == idContrat
                and paye.getMois() == mois
                and paye.getAnnee() == annee
            ):
                # print(f"connnnn: {idContrat }  locaaa: {idLocataire} montant: {paye.getMontant()} ")
                somme += paye.getMontant()
        return somme


p = PayementBox()
# x = p.getLastPayementByContrat(2)
s = p.getPayerByIdLocationIdBox("Loc1", "B1", 1, 5, 2024)
# print(s)

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
        montant: float,
        payementMois: int,
        payementAnnee: int,
    ):
        montant *= Echelle.valeur
        print(
            f"Miantso ********************* mois: {mois} annee: {annee} idLocataire: {idLocataire}"
        )
        tempLocataire = Locataire()
        tempLocataire = tempLocataire.getById(idLocataire=idLocataire)
        tempBox = Box()
        tempMarcherBox = MarcherBox()
        allMarcherBox = tempMarcherBox.getAll()
        tempMarcher = Marcher()

        allSortedContrat = tempLocataire.getAncienContrat()
        for contrat in allSortedContrat:
            marcher = None
            contratBox = tempBox.getById(contrat.getIdBox())
            for marcherBox in allMarcherBox:
                if marcherBox.getIdBox() == contrat.getIdBox():
                    marcher = tempMarcher.getById(marcherBox.getIdMarcher())
                    break
            contrat.initMois(marcher, contratBox)

        moisApayer = None
        for contrat in allSortedContrat:
            for contratMois in contrat.getMois():
                pourcentageMois = (
                    float(contratMois.getVoaloha())
                    / float(contratMois.getTokonyAloha())
                ) * 100
                if pourcentageMois != 100:
                    moisApayer = contratMois
                    # print(f"HELLLLO {moisApayer.getValeur() } {moisApayer.getAnnee()} {moisApayer.getContrat().getIdContrat()}")
                    break
            for oderContrat in allSortedContrat:
                if contrat.getIdContrat() != oderContrat.getIdContrat():
                    for orderContratMois in oderContrat.getMois():
                        pourcentageMois = (
                            float(orderContratMois.getVoaloha())
                            / float(orderContratMois.getTokonyAloha())
                        ) * 100
                        if pourcentageMois != 100:
                            dateContrat = date(
                                moisApayer.getAnnee(), moisApayer.getValeur(), 1
                            )
                            dateOderContrat = date(
                                orderContratMois.getAnnee(),
                                orderContratMois.getValeur(),
                                1,
                            )
                            if dateContrat > dateOderContrat:
                                moisApayer = orderContratMois
                                break

        if moisApayer:
            hisContrat = moisApayer.getContrat()
            print(
                f"**debug Le mois a payer est: {moisApayer.getValeur() } {moisApayer.getAnnee()} tokonyAloha: {moisApayer.getTokonyAloha()}"
            )
            print(
                f"**debug  idLocataire: {hisContrat.getIdLocataire()} idBox: {hisContrat.getIdBox()} idContrat: {hisContrat.getIdContrat()} {moisApayer.getAnnee()} montant: {montant}"
            )
            print(f"tempMontant {montant}")
            reste = (float(montant) + float(moisApayer.getVoaloha())) - float(
                moisApayer.getTokonyAloha()
            )
            if reste == 0:
                montant -= reste
                self.payer(
                    idLocataire=idLocataire,
                    idBox=hisContrat.getIdBox(),
                    idContrat=hisContrat.getIdContrat(),
                    mois=moisApayer.getValeur(),
                    annee=moisApayer.getAnnee(),
                    montant=montant,
                    payementMois=payementMois,
                    payementAnnee=payementAnnee,
                )
            elif reste > 0:
                print(f"Misy reste {reste}")
                print(f"ito zany no aloha ato {montant - reste}")
                # raise Exception (f"misy reste e{reste}")
                self.payer(
                    idLocataire=idLocataire,
                    idBox=hisContrat.getIdBox(),
                    idContrat=hisContrat.getIdContrat(),
                    mois=moisApayer.getValeur(),
                    annee=moisApayer.getAnnee(),
                    montant=montant - reste,
                    payementMois=payementMois,
                    payementAnnee=payementAnnee,
                )
                self.insertPayementBox(
                    idLocataire,
                    mois,
                    annee,
                    reste,
                    payementMois,
                    payementAnnee,
                )
            elif reste < 0:
                self.payer(
                    idLocataire=idLocataire,
                    idBox=hisContrat.getIdBox(),
                    idContrat=hisContrat.getIdContrat(),
                    mois=moisApayer.getValeur(),
                    annee=moisApayer.getAnnee(),
                    montant=montant,
                    payementMois=payementMois,
                    payementAnnee=payementAnnee,
                )
                return

        print(f"Nombre de contrat:{len(allSortedContrat)}")
        for contrat in allSortedContrat:
            print(
                f"Contrat: {contrat.getIdContrat()} idBox: {contrat.getIdBox()}  idLocataire: {contrat.getIdLocataire()}"
            )
            for mois in contrat.getMois():
                print(
                    f"{mois.getValeur()} { mois.getAnnee() }  {mois.getVoaloha()} {mois.getTokonyAloha()}  => {(float(mois.getVoaloha()) / float(mois.getTokonyAloha()) * 100)}"
                )

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

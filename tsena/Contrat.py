from matplotlib.dates import relativedelta
from connection.Connection import *
from datetime import *
from fonction.Fonction import Fonction


class Contrat:
    def __init__(
        self,
        idContrat=None,
        idBox=None,
        idLocataire=None,
        moisDebut=None,
        anneeDebut=None,
        moisFin=None,
        anneeFin=None,
        dateSignature=None,
    ):
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

    def setMoisDebut(self, mois: int):
        self.__moisDebut = mois

    def setAnneeDebut(self, annee: int):
        self.__anneeDebut = annee

    def setMoisFin(self, mois: int):
        self.__moisFin = mois

    def setAnneeFin(self, annee: int):
        self.__anneeFin = annee

    def setDateSignature(self, date):
        self.__dateSignature = date

    def getById(self, idContrat):
        objet = None
        query = "SELECT * FROM contrat WHERE idContrat = ?"
        objetSql = Connection.getExecute(query, (idContrat,))
        if objetSql:
            objet = Contrat(
                objetSql[0][0],
                objetSql[0][1],
                objetSql[0][2],
                objetSql[0][3],
                objetSql[0][4],
                objetSql[0][5],
                objetSql[0][6],
                objetSql[0][7],
            )
        return objet

    def getAll(self):
        allObjet = []
        query = "SELECT idContrat FROM contrat"
        contratSql = Connection.getExecute(query)
        for line in contratSql:
            tempObjet = self.getById(line[0])
            allObjet.append(tempObjet)
        return allObjet

    def insert(self, idLocataire, idBox):
        allContrat = self.getAll()
        for contrat in allContrat:
            dateDebut_contrat = date(contrat.getAnneeDebut(), contrat.getMoisDebut(), 1)
            dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
            dateFin_contrat = dateFin_contrat - relativedelta(months=1)

            dateDebut_nouveau = date(self.__anneeDebut, self.__moisDebut, 1)
            dateFin_nouveau = date(self.__anneeFin, self.__moisFin, 1)

            if (
                Fonction.intersectDate(
                    dateDebut_contrat, dateFin_contrat, dateDebut_nouveau
                )
                or Fonction.intersectDate(
                    dateDebut_contrat, dateFin_contrat, dateFin_nouveau
                )
                or Fonction.intersectDate(
                    dateDebut_nouveau, dateFin_nouveau, dateDebut_contrat
                )
                or Fonction.intersectDate(
                    dateDebut_nouveau, dateFin_nouveau, dateFin_contrat
                )
            ):
                # print(f" {contrat.getIdContrat()} {contrat.getIdLocataire()} {contrat.getIdBox()}")
                # print(f"{idBox} {idLocataire}")
                
                if  (contrat.getIdBox() == idBox or contrat.getIdLocataire() != idLocataire):
                    raise ValueError(
                        f"Les dates du contrat chevauchent un contrat existant pour la box {contrat.getIdBox()}\n{contrat.getIdLocataire()}."
                    )

        query = "INSERT INTO contrat (idBox, idLocataire, moisDebut, anneeDebut, moisFin, anneeFin, dateSignature) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (
            self.__idBox,
            self.__idLocataire,
            self.__moisDebut,
            self.__anneeDebut,
            self.__moisFin,
            self.__anneeFin,
            self.__dateSignature,
        )
        Connection.execute(query, params)

    def update(self):
        query = "UPDATE contrat SET idBox = ?, idLocataire = ?, moisDebut = ?, anneeDebut = ?, moisFin = ?, anneeFin = ?, dateSignature = ? WHERE idContrat = ?"
        params = (
            self.__idBox,
            self.__idLocataire,
            self.__moisDebut,
            self.__anneeDebut,
            self.__moisFin,
            self.__anneeFin,
            self.__dateSignature,
            self.__idContrat,
        )
        Connection.execute(query, params)

    def delete(self):
        query = "DELETE FROM contrat WHERE idContrat = ?"
        Connection.execute(query, (self.__idContrat,))

    def getContratByIdBox(self, idBox: str, mois: int, annee: int):
        allContrats = self.getAll()
        dateVerify = date(annee, mois, 1)

        for contrat in allContrats:
            if contrat.getIdBox() == idBox:
                dateDebut_contrat = date(
                    contrat.getAnneeDebut(), contrat.getMoisDebut(), 1
                )
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                dateFin_contrat = dateFin_contrat - relativedelta(months=1)
                if Fonction.intersectDate(
                    dateDebut_contrat, dateFin_contrat, dateVerify
                ):
                    return contrat
        return None

    def arretContrat(self, idLocataire, idBox, moisArret, anneeArret):
        allContrats = self.getAll()
        dateArret = date(anneeArret, moisArret, 1)
        for contrat in allContrats:
            if contrat.getIdBox() == idBox and contrat.getIdLocataire() == idLocataire:
                dateDebut_contrat = date(
                    contrat.getAnneeDebut(), contrat.getMoisDebut(), 1
                )
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if dateDebut_contrat < dateArret < dateFin_contrat:
                    # print(f"afaka miala {dateFin_contrat}")
                    contrat.setMoisFin(dateArret.month)
                    contrat.setAnneeFin(dateArret.year)
                    contrat.setDateSignature(date.today())
                    contrat.update()
        raise Exception("Pour annuler le contrat il faut etre dans le contrat")

    def geContratByLocaBox(self, idLocataire, idBox, mois: int, annee: int):
        dateVerifie = date(annee, mois, 1)
        tempcontrat = Contrat()
        allContrat = tempcontrat.getAll()

        for contrat in allContrat:
            if contrat.getIdLocataire() == idLocataire and contrat.getIdBox() == idBox:
                dateDebut_contrat = date(
                    contrat.getAnneeDebut(), contrat.getMoisDebut(), 1
                )
                dateFin_contrat = date(contrat.getAnneeFin(), contrat.getMoisFin(), 1)
                if Fonction.intersectDate(
                    dateDebut_contrat, dateFin_contrat, dateVerifie
                ):
                    return contrat
        return None


# tempContrat = Contrat()
# tempContrat.arretContrat("Loc1" , "B1" , 12 , 2024)

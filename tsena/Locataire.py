from connection.Connection import Connection

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

   
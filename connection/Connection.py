import pyodbc

class Connection:
    dbFile = r'E:\ITU\L2\S4\INF\Prog\Marcher\sql\marcher.accdb'
    connStr = rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={dbFile}'
    conn = None

    @classmethod
    def init(cls):
        """Initialise la connexion une seule fois"""
        if cls.conn is None:
            try:
                cls.conn = pyodbc.connect(cls.connStr)
                print("Connexion à la base de données réussie.")
            except Exception as e:
                print(f"Erreur de connexion à la base de données : {e}")

    @classmethod
    def getExecute(cls, query, params=None):
        """Exécute une requête SELECT et retourne les résultats"""
        # cls.ensure_connection()
        try:
            with cls.conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None

    @classmethod
    def execute(cls, query, params=None):
        """Exécute une requête INSERT, UPDATE ou DELETE"""
        # cls.ensure_connection()
        try:
            with cls.conn.cursor() as cursor:
                cursor.execute(query, params or ())
                cls.conn.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return False

    @classmethod
    def ensure_connection(cls):
        """Vérifie et rétablit la connexion si nécessaire"""
        if cls.conn is None or cls.conn.closed:
            print("Reconnecter à la base de données...")
            cls.init()
    @classmethod
    def testConnection (cls):
        if cls.conn is None or cls.conn.closed:
            raise Exception ("Connexion non etablie :(")
    @classmethod
    def close(cls):
        """Ferme proprement la connexion"""
        if cls.conn:
            cls.conn.close()
            cls.conn = None
            print("Connexion fermée.")




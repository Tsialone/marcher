import pyodbc

class Connection:
    dbFile = r'E:\ITU\L2\S4\INF\Prog\Marcher\sql\marcher.accdb'
    connStr = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + dbFile
    @classmethod
    def getExecute(cls, query, params=None):
        rows = None
        try:
            with pyodbc.connect(cls.connStr) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    rows = cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
        return rows

    @classmethod
    def execute(cls, query, params=None):
        try:
            with pyodbc.connect(cls.connStr) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error executing query: {e}")
            return False
import pyodbc
from prettytable import PrettyTable

def execute_sql_file(access_db_path, sql_file_path):
    """Exécute un fichier .sql sur une base Microsoft Access via ODBC et affiche les résultats des SELECT de façon propre"""
    try:
        # Connexion à la base de données Access
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + access_db_path
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Lire le fichier SQL
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Exécuter les requêtes une par une
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:  # Ignorer les requêtes vides
                if statement.strip().lower().startswith("select"):
                    # Pour les requêtes SELECT, afficher les résultats proprement
                    cursor.execute(statement)
                    rows = cursor.fetchall()

                    # Créer un tableau PrettyTable avec les noms de colonnes
                    columns = [desc[0] for desc in cursor.description]  # Noms des colonnes
                    table = PrettyTable(columns)

                    # Ajouter les lignes (même si aucune ligne, afficher le tableau avec les colonnes)
                    if rows:
                        for row in rows:
                            table.add_row(row)
                    else:
                        # Ajouter une ligne vide pour indiquer qu'il n'y a pas de résultats
                        table.add_row(["Aucun résultat trouvé" for _ in columns])

                    print(table)
                else:
                    # Exécuter les autres types de requêtes (ex. CREATE, INSERT, etc.)
                    cursor.execute(statement)
                    conn.commit()
                    print(f"✅ Requête exécutée : {statement}")

        print(f"✅ Fichier '{sql_file_path}' exécuté avec succès sur la base Access.")

    except Exception as e:
        print(f"❌ Erreur : {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    # Demander le chemin du fichier Access et du fichier SQL
    access_db_path = r'E:\ITU\L2\S4\INF\Prog\Marcher\sql\marcher.accdb'
    sql_file_path = input("Entrez le chemin du fichier .sql : ").strip()

    execute_sql_file(access_db_path, "sql/"+sql_file_path + ".sql")

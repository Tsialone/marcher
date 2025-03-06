from datetime import *

class Fonction:
    def displayTab (rows):
        for row in rows:
            print(row)
    def trieDate(listDate, asc=True):
        try:
            if not all(isinstance(date_obj, date) for date_obj in listDate):
                raise TypeError("Tous les éléments de listDate doivent être des objets datetime.date")
            sorted_dates = sorted(listDate, reverse=not asc)
            return sorted_dates
        except TypeError as e:
            print(f"Erreur : {e}")
            return []
    def parse_date_mmaaaa(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%m-%Y")
            return date_obj.date()
        except Exception as e:
            raise Exception (e)
    def intersectDate (datex , datey , dateVerify):
        if datex <= dateVerify <= datey:
            return True
        else:
            return False
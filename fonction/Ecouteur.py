from datetime import date
import tkinter as tk
from tkinter import messagebox
from tsena.PayementBox import PayementBox
import traceback
from fonction.Data import Data
from fonction .Fonction import Fonction
from tsena.Contrat import Contrat
import pyodbc



class Ecouteur:
    # def continuite ():
    #     response= messagebox.askquestion ("Confirmation" , "Vous navez pas encore payer .... payer mantenant?" )
    #     if response:
    #         raise Exception ("Veuillez payer d'abord .... impayer\n 2003/02/20")
    moisMapping = {
            "Janvier": 1,
            "Fevrier": 2,
            "Mars": 3,
            "Avril": 4,
            "Mai": 5,
            "Juin": 6,
            "Juillet": 7,
            "Aout": 8,
            "Septembre": 9,
            "Octobre": 10,
            "Novembre": 11,
            "Decembre": 12,
            }
    def payementBlock(idBox,mois, annee , montant):
        try:
            idBox =idBox.get()
            mois = Ecouteur.moisMapping[mois.get()]
            annee = int(annee.get())
            montant = float(montant.get())
            payement = PayementBox()
            payement.insertPayementBox(idBox=idBox , mois=mois , annee=annee , montant= montant)
            # Ecouteur.continuite()
            messagebox.showinfo("Success", f"Payement reussi")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())

    def verification(mois, annee):
        try:
            mois = Ecouteur.moisMapping[mois.get()]
            annee = int(annee.get())
            Data.changeColor(mois=mois  , annee=annee)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())
    def makeContrat(idLocataire, idBox, dateDebut, dateFin):
        try:
            idLocataire_str = str(idLocataire.get())
            idBox_str = str(idBox.get())
            dateDebut_obj = Fonction.parse_date_mmaaaa(str(dateDebut.get()))
            dateFin_obj = Fonction.parse_date_mmaaaa(str(dateFin.get()))

             
            if dateDebut_obj > dateFin_obj:
                raise Exception(f"La date de début ({dateDebut_obj}) doit être antérieure ou égale à la date de fin ({dateFin_obj}).")
            if dateDebut_obj < Data.dateExercice or dateFin_obj < Data.dateExercice:
                raise Exception("Le payement ne doit pas etre avant l'exercice " + str(Data.dateExercice) )
                
            # Extraire mois et année
            moisDebut = dateDebut_obj.month
            anneeDebut = dateDebut_obj.year
            moisFin = dateFin_obj.month
            anneeFin = dateFin_obj.year

            # Date de signature
            dateSignature = date.today()

            # Créer un objet Contrat
            contrat = Contrat(idBox=idBox_str, idLocataire=idLocataire_str, moisDebut=moisDebut, anneeDebut=anneeDebut, moisFin=moisFin, anneeFin=anneeFin, dateSignature=dateSignature)

            # Insérer le contrat dans la base de données
            contrat.insert()
            messagebox.showinfo("Success", f"Contrat effectuer")
            

            # messagebox.showinfo("Succès", "Contrat inséré avec succès.")
        except Exception as e:  # Capture les autres exceptions
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())
            
    
        
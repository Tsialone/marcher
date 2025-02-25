import tkinter as tk
from tkinter import messagebox
from tsena.Box import *
from tsena.PayementBox import PayementBox
import traceback

from fonction.Data import Data



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

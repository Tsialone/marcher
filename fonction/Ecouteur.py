from datetime import date
import tkinter as tk
from tkinter import messagebox
from tsena.PayementBox import PayementBox
import traceback
from fonction.Data import Data
from fonction.Fonction import Fonction
from tsena.Contrat import Contrat
import pyodbc
from tsena.MarcherBox import MarcherBox
from tsena.Locataire import Locataire
from tsena.Marcher import Marcher
from tsena.Box import Box
from decimal import Decimal, getcontext
getcontext().prec = 10


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
    moisMapping_reverse = {
        1: "Janvier",
        2: "Fevrier",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Aout",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Decembre",
    }

    def payementBlock(
        idLocataire, mois, annee, montant, payementMois, payementAnnee
    ):
        try:

            idLocataire = idLocataire.get()
            mois = Ecouteur.moisMapping[mois.get()]
            annee = int(annee.get())

            payementMois = Ecouteur.moisMapping[payementMois.get()]
            payementAnnee = int(payementAnnee.get())

            print(f"Ito zah ito ee {payementMois} {payementAnnee}")

            montant = Decimal (str(montant.get()))
            payement = PayementBox()
            payement.insertPayementBox(
                idLocataire=idLocataire,
                mois=mois,
                annee=annee,
                montant=montant,
                payementMois=  payementMois , 
                payementAnnee= payementAnnee
            )
            # Ecouteur.continuite()
            messagebox.showinfo("Success", f"Payement reussi")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())

    def verification(mois, annee):
        try:
            mois = Ecouteur.moisMapping[mois.get()]
            annee = int(annee.get())
            Data.changeColor(mois=mois, annee=annee)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())

    def dette(mois, annee , formulaire):
        try:
            mois = Ecouteur.moisMapping[mois.get()]
            annee = int(annee.get())
            tempLocataire   =  Locataire()
            allLocataire = tempLocataire.getAll()
            deco = [
            ]
            
            
            
            dateAvoir  = date (annee , mois , 1)
            box_dict = {box.getIdBox(): box for box in Box().getAll()}
            marcherBox_list = MarcherBox().getAll()
            marcherBox_dict = {mb.getIdBox(): mb for mb in marcherBox_list}
            marcher_dict = {}
            
            for locataire in allLocataire:
                hisDette = 0
                print(f"----------------------Locataire: {locataire.getIdLocataire()}--------------------------")
                allSortedContrat = locataire.getAncienContrat()
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
                for detteContrat in allSortedContrat:
                    if date (detteContrat.getAnneeDebut() , detteContrat.getMoisDebut() , 1) < dateAvoir:
                        hisMois = contrat.getMois()
                        if hisMois:
                            for mois in hisMois:
                                tsyVoaloha  = mois.getTokonyAloha() - mois.getVoaloha()
                                hisDette += tsyVoaloha
                                # print(f"{mois.getValeur()} {mois.getAnnee()}")
                deco.append ({"idLocataire":locataire.getIdLocataire()   , "dette":hisDette})

                    
            
                
                
           
            
            formulaire.textDette (deco)
            

            # Insérer le contrat dans la base de données
            # messagebox.showinfo("Success", f"Contrat effectuer")

            # messagebox.showinfo("Succès", "Contrat inséré avec succès.")
        except Exception as e:  # Capture les autres exceptions
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
            print(traceback.format_exc())

from connection.Connection import Connection
Connection.init()
from fonction.Fonction import *
from tsena.Marcher import Marcher
from tsena.MarcherBox import MarcherBox
from tsena.PayementBox import *
from aff.Fenetre import *
from aff.Carte import *
from form.Rectangle import *
import tkinter as tk
from aff.Formulaire import Formulaire
from tsena.Box import Box
from fonction.Data import Data


    
    


fenetre = Fenetre("1200x700" ,"Marhcer")
carte  = Carte(700 , 670 , fenetre)
formulaire = Formulaire(480 , 670 , fenetre)
Data.allMarcher = Data.tempMarcher.getAll()
Data.fenetre = fenetre

Data.carte  =carte
Data.drawMarcher(carte)
Data.drawTextMarcher()


    

fenetre.mainloop()

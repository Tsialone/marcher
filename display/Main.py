try:
    from connection.Connection import Connection
    Connection.init()
    from fonction.Fonction import *
    from tsena.Marcher import Marcher
    from tsena.MarcherBox import MarcherBox
    from tsena.PayementBox import *
    from display.Fenetre import *
    from display.Carte import *
    from form.Rectangle import *
    import tkinter as tk
    from display.Formulaire import Formulaire
    from tsena.Box import Box
    from fonction.Data import Data
    
    
    fenetre = Fenetre("1200x700" ,"Marhcer")
    carte  = Carte(870 , 670 , fenetre)
    formulaire = Formulaire(600 , 670 , fenetre)
    
    
    
    Data.allMarcher = Data.tempMarcher.getAll()
    Data.fenetre = fenetre

    Data.carte  =carte
    Data.drawMarcher(carte)
    Data.drawTextMarcher()
    fenetre.mainloop()

finally:
    Connection.close()



    





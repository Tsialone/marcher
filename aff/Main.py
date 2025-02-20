from connection.Connection import Connection
from fonction.Fonction import *
from tsena.Marcher import *
from tsena.Box import *
from tsena.MarcherBox import *
from tsena.PayementBox import *
from aff.Fenetre import *
from aff.Carte import *
from aff.Formulaire import *
from form.Rectangle import *






print("Test")
tempMarcher = Marcher ()
tempBox = Box ()
tempMarcherBox=  MarcherBox ()
tempPayementBox = PayementBox()

allMarcher = tempMarcher.getAll()
allBox = tempBox.getAll()
allMarcherBox = tempMarcherBox.getAll()
allPayementBox =  tempPayementBox.getAll()

try:
    tempPayementBox.insertPayementBox("B1" , 12 , 2023)
except ValueError as e:
    print(e)

fenetre = Fenetre("1200x700" ,"Marhcer")
carte  = Carte(700 , 670 , fenetre)
formulaire = Formulaire(420 , 670 , fenetre)
# Créer un canevas
canvas = tk.Canvas(carte, width=680, height=650, bg="white")
canvas.place(x=10 , y=10)

# Créer un rectangle
rect = Rectangle(0, 50, 200, 100, "blue")
rect2 = Rectangle(0, 100, 50, 100, "red")


# Dessiner le rectangle
rect.draw(canvas)
rect2.draw(canvas)

fenetre.mainloop()

from tkinter import messagebox
import math


class Mouse:
    gauche = None
    @staticmethod 
    def clickGauche (event , marcher):
        Mouse.gauche = (event.x, event.y)

    # Assuming marcher.getBoxs() returns a list of boxes
        for box in marcher.getBoxs():
            # boxCentre = (box.getLargeur() / 2, box.getLongueur() / 2)
            # x1, y1 = boxCentre
            # x2, y2 = Mouse.gauche
            if box.contains_point (Mouse.gauche):
                messagebox.showinfo("click", f"vous avez cliqué gauche à {box.getIdBox()}")
                
                # print(f"{box.getIdBox()} x={box.get_x()} y={box.get_y()}")
            
            # Calculate the distance between the center of the box and the mouse click position
            # distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
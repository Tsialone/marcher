from tkinter import messagebox


class Mouse:
    droite = None
    @staticmethod 
    def clickGauche (event):
        Mouse.droite = (event.x , event.y)
        # messagebox.showinfo("click" , f"vous avez clik gauche " +  str (Mouse.mousePoint))
        # allMarcher = Data.allMarcher
        # for marcher in allMarcher:
        #     for box in marcher.getBoxs():
        #         if (box.contains(Mouse.mousePoint)):
        #             messagebox.showinfo(str(box.getIdBox()) , "")gi
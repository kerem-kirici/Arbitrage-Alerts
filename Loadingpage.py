import tkinter as tk
from PIL import ImageTk, Image

class LoadingPage(tk.Frame):

    __ID = 'LoadingPage'

    def __init__(self, parent, controller):
        super().__init__(parent, bg='#A6F3FE')

        img_path = '.\\photos\\icons\\icon1\\Arbitraj-logos.png'
        img = Image.open(img_path).resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        img_lbl = tk.Label(self, image=img, bg='#A6F3FE')
        img_lbl.image=img
        img_lbl.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(self, text='Setting Backend Applications..', font=('Times', '20', 'bold'),
                 bg='#A6F3FE').pack(side=tk.TOP, fill=tk.BOTH)
        tk.Label(self, text='Do NOT quit program! This may take about 30 seconds. Thanks for your patience!', font=('Times', '9'),
                 bg='#A6F3FE').pack(side=tk.TOP, fill=tk.BOTH)

        # add Enter key press as an 'Add' button press

    @property
    def id(self):
        return self.__ID

    def __str__(self):
        return self.__ID


class WelcomePage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg='#A6F3FE')

        img_path = '.\\photos\\icons\\icon1\\Arbitraj-logos.png'
        img = Image.open(img_path).resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        img_lbl = tk.Label(self, image=img, bg='#A6F3FE')
        img_lbl.image=img
        img_lbl.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(self, text='Welcome! Setting Backend Applications..', font=('Times', '20', 'bold'),
                 bg='#A6F3FE').pack(side=tk.TOP, fill=tk.BOTH)
        tk.Label(self, text='Do NOT quit the program! This may take about 30 seconds. Thanks for your patience!', font=('Times', '9'),
                 bg='#A6F3FE').pack(side=tk.TOP, fill=tk.BOTH)

        # add Enter key press as an 'Add' button press

import tkinter as tk

class Popup(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent, bg='#A6F3FE')  

        self.__alert_value = None


        main_screen_frame = tk.Frame(self, bg='#A6F3FE')

        entry_frame = tk.Frame(main_screen_frame, bg='#A6F3FE')

        tk.Label(entry_frame, text='Alert at:', font=('Times', '16', 'bold'), bg='#A6F3FE').pack(side=tk.LEFT, fill=tk.BOTH)

        self.__alert_entry = tk.Entry(entry_frame, font=('Times', '16', 'bold'), bg='#A6F3FE', bd=2)
        self.__alert_entry.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.__alert_entry.focus()

        entry_frame.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Button(main_screen_frame, text='Add', font=('Times', '13', 'bold'), bg='#A6F3FE', activebackground='#90E9F7', padx=10, bd=3,
                  command=self.__add).pack(side=tk.RIGHT)

        self.bind('<Return>', lambda *args: self.__add())

        main_screen_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.not_valid_text_label = None

        # add Enter key press as an 'Add' button press

    @property
    def alert_value(self):
        return self.__alert_value
    

    def __add(self):
        # write some real code you goddamn genius
        self.__alert_value = self.__alert_entry.get()

        if self.__valid():
            self.destroy()
        else:
            if self.not_valid_text_label is None:
                self.not_valid_text_label = tk.Label(self, text='Invalid entry. Enter a floating number or integer.',
                                                     font=('Times', '10', 'italic'), bg='#A6F3FE', fg='red')
                self.not_valid_text_label.pack(side=tk.BOTTOM, fill=tk.X)
            else:
                self.not_valid_text_label.config(text='Again, invalid entry. Enter a floating number or integer.')

    def __valid(self):
        try:
            self.__alert_value = float(self.__alert_value)
            return True
        except:
            return False



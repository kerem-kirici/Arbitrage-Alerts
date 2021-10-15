from Backend import Backend
from Mainpage import MainPage
from Settingspage import SettingsPage
from Notifspage import NotificationsPage
from Loadingpage import LoadingPage, WelcomePage
import tkinter as tk
import time
import os
from datetime import datetime


APP_ICON_PATH = '.\\photos\\icons\\icon2\\Arbitraj.png'
APP_TITLE = 'Arbitraj'


class Application(tk.Tk):


    def __init__(self, headless=True, log=False, *args, **kwargs):

        self.console_display = log
        self.headless = headless
        super().__init__(*args, **kwargs)
        self.title(APP_TITLE)

        self.iconphoto(False, tk.PhotoImage(file=APP_ICON_PATH))
        self.geometry('508x294')
        self.resizable(False, False)


        start_frame = tk.Frame(master=self, width=500, height=280, relief=tk.GROOVE, borderwidth=10, background='#A6F3FE')  # (#A6F3FE)

        start_page = WelcomePage(start_frame)

        start_page.grid(row=0, column=0, sticky='nsew')

        start_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.update()
        self.__set_backend()

        start_frame.pack_forget()
        start_frame.destroy()

        container = tk.Frame(master=self, width=500, height=280, relief=tk.GROOVE, borderwidth=10, background='#A6F3FE')  # (#A6F3FE)

        self.frames = {}
        
        for frame_page in (MainPage, SettingsPage, NotificationsPage, LoadingPage):

            frame = frame_page(container, self)

            self.frames[frame_page.id] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.active_frame = MainPage.id
        self.refresh()
        self.show_main_page()


    def refresh(self):

        if self.active_frame == MainPage.id:
            self.backend_application.refresh()

            # refresh price data on the screen
            frame = self.frames[self.active_frame]
            frame.refresh_data()
            
        elif self.active_frame == NotificationsPage.id:
            self.backend_application.refresh()

            frame = self.frames[self.active_frame]
            frame.refresh_notifications()

        if self.console_display:
            print(self.backend_application.last_refresh_date)
            print(self.backend_application.UsdTry_Price)
            print(self.backend_application.price_table)
            print(repr(self.backend_application), end='\n\n')

        self.after(900, self.refresh)

    def remove_notification(self):
        if self.active_frame == NotificationsPage.id:
            frame = self.frames[self.active_frame]
            selected_notifications = sorted(frame.notifictaions_listbox.curselection(), reverse=True)
            # reverse=True is for not changing indexes for further indexes while removing the top ones
            sorted_all_notifications = sorted(frame.notifications, key=lambda x: (datetime.now()-x[1]).total_seconds())
            for notif_index in selected_notifications:
                notification = sorted_all_notifications[notif_index]
                self.backend_application.remove_notification(notification)
                frame.notifications.remove(notification)
                frame.notifictaions_listbox.delete(notif_index)

    def set_markets(self, Market1_name, Market2_name):
        # you need to make a loading page and remaining time label while changing markets and also try to make this for start of the application 
        self.show_loading_page()
        self.update()
        market1_id = self.backend_application.market_name_id_table[Market1_name]
        market2_id = self.backend_application.market_name_id_table[Market2_name]
        self.backend_application.set_markets(market1_id, market2_id)
        self.active_frame = MainPage.id
        self.refresh()
        self.show_main_page()


    def __set_backend(self):
        self.backend_application = Backend(headless=self.headless)


    def show_main_page(self):
        page_id = MainPage.id
        self.active_frame = page_id
        frame = self.frames[page_id]
        frame.refresh_data()
        frame.tkraise()

    def show_notif_page(self):
        page_id = NotificationsPage.id
        self.active_frame = page_id
        frame = self.frames[page_id]
        frame.refresh_notifications()
        frame.tkraise()

    def show_settings_page(self):
        page_id = SettingsPage.id
        self.active_frame = page_id
        frame = self.frames[page_id]
        frame.refresh_data()
        frame.tkraise()

    def show_loading_page(self):
        page_id = LoadingPage.id
        self.active_frame = page_id
        frame = self.frames[page_id]
        frame.tkraise()



if __name__ == '__main__':

    app = Application(log=False)

    app.mainloop()
    app.backend_application.close()

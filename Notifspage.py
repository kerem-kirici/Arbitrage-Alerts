import tkinter as tk

from datetime import datetime



class NotificationsPage(tk.Frame):

    __ID = 'NotificationsPage'

    def __init__(self, parent, controller):        
        super().__init__(parent, bg='#A6F3FE')

        self.controller = controller        
        self.notifications = set()

        tk.Label(self, text='Arbitrage Notifications', font=('Helvetica', '14', 'italic'),
                 bg='#A6F3FE').grid(row=0, column=1, columnspan=4, padx=10, pady=4, sticky='nse')

        tk.Button(self, text='\u2190', font=('Times', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.show_main_page).grid(row=0, column=0, sticky='nsw', padx=10, pady=4)


        notifications_frame = tk.Frame(self, relief=tk.GROOVE, bg='#A6F3FE')

        scrollbar = tk.Scrollbar(notifications_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notifictaions_listbox = tk.Listbox(notifications_frame, bg='#90E9F7', bd=5, width=54, yscrollcommand=scrollbar.set,
                                                height=9, font=('Times', '12'), selectbackground='#4116AC', selectmode=tk.MULTIPLE)  #4116AC
        self.notifictaions_listbox.pack(side=tk.TOP, fill=tk.BOTH)

        scrollbar.config(command=self.notifictaions_listbox.yview)

        notifications_frame.grid(row=1, column=0, columnspan=5, rowspan=5, padx=10, pady=(0, 4), sticky='we')


        tk.Button(self, text='Delete', font=('Calibri', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.remove_notification).grid(row=6, column=0, sticky='ew', padx=10, pady=(0, 4))

        tk.Button(self, text='Exit', font=('Calibri', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.destroy).grid(row=6, column=4, sticky='ew', padx=10, pady=(0, 4))

    def refresh_notifications(self):
        notifications = self.controller.backend_application.notifications
        if self.notifications != notifications:
            for (notification, notification_time) in sorted(notifications - self.notifications,
                                                            key=lambda x: (datetime.now()-x[1]).total_seconds(), reverse=True):
                self.notifictaions_listbox.insert(0, notification_time.strftime('%H:%M:%S') + ' \u2192 ' + notification)
                self.notifications.add((notification, notification_time))

    @property
    def id(self):
        return self.__ID
        
    def __str__(self):
        return self.__ID


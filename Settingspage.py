import tkinter as tk
from Popuppage import Popup


class SettingsPage(tk.Frame):

    __ID = 'SettingsPage'

    def __init__(self, parent, controller):
        super().__init__(parent, bg='#A6F3FE')
        
        self.controller = controller
        self.commands = list()
        self.tmp_alerts = list()

        tk.Button(self, text='\u2715', font=('Helvetica', '12', 'bold'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.cancel_settings).grid(row=0, column=0, sticky='nsw', padx=10, pady=4)

        tk.Label(self, text='Settings', font=('Helvetica', '14'),
                 bg='#A6F3FE').grid(row=0, column=1, columnspan=3, padx=10, pady=4, sticky='nsew')

        tk.Button(self, text='\u2714', font=('Helvetica', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.save_settings).grid(row=0, column=4, sticky='nse', padx=10, pady=4)

        # Alerts
        alerts_frame = tk.Frame(self, relief=tk.GROOVE, bg='#A6F3FE', borderwidth=4)

        tk.Label(alerts_frame, text='Alerts', font=('Helvetica', '12', 'bold'),
                 bg='#A6F3FE', relief=tk.RAISED, borderwidth=3).grid(row=0, column=0, columnspan=5, padx=5, pady=0, sticky='ew')

        alerts_listbox_frame = tk.Frame(alerts_frame, relief=tk.FLAT, bg='#A6F3FE')
        scrollbar = tk.Scrollbar(alerts_listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.alerts_listbox = tk.Listbox(alerts_listbox_frame, bg='#90E9F7', bd=3, width=17, yscrollcommand=scrollbar.set,
                                                height=5, font=('Calibri', '12'), selectbackground='#4116AC', selectmode=tk.MULTIPLE)  #4116AC
        self.alerts_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.alerts_listbox.yview)

        alerts_listbox_frame.grid(row=1, column=0, rowspan=2, columnspan=2, sticky='nsew', padx=9, pady=2)

        # Buttons
        tk.Button(alerts_frame, text='Add', font=('Helvetica', '11'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.add_alert).grid(row=1, column=2, sticky='new', padx=5, pady=5)

        tk.Button(alerts_frame, text='Remove', font=('Helvetica', '11'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.remove_selected_alerts).grid(row=2, column=2, sticky='new', padx=5, pady=5)

        alerts_frame.grid(row=1, column=0, columnspan=3, rowspan=4, padx=(10, 0), pady=(0, 4), sticky='nsew')

        # Markets
        markets_frame = tk.Frame(self, relief=tk.GROOVE, bg='#A6F3FE', borderwidth=4)

        tk.Label(markets_frame, text='Markets', font=('Helvetica', '12', 'bold'),
                 bg='#A6F3FE', relief=tk.RAISED, borderwidth=3).grid(row=0, column=0, columnspan=2, padx=5, pady=0, sticky='ew')

        # Market 1
        tk.Label(markets_frame, text='Market 1:', font=('Helvetica', '11', 'bold'),
                 bg='#A6F3FE').grid(row=1, column=0, padx=(5, 2), pady=(0, 5), sticky='nsew')

        self.selected_market_1 = tk.StringVar()
        self.selected_market_1.set('Market1')

        options = self.controller.backend_application.market_options

        dropdown_markets_1 = tk.OptionMenu(markets_frame, self.selected_market_1, *options)
        dropdown_markets_1.config(width=10)
        dropdown_markets_1.config(bg='#A6F3FE', activebackground='#90E9F7', borderwidth=2, relief=tk.RAISED, highlightthickness=0,
                                  font=('Helvetica', '10', 'italic bold'))
        dropdown_markets_1['menu'].config(bg='#90E9F7', font=('Helvetica', '10', 'italic bold'))
        dropdown_markets_1.grid(row=1, column=1, padx=(2, 5), pady=(0, 5), sticky='nsew')

        # Market 2
        tk.Label(markets_frame, text='Market 2:', font=('Helvetica', '11', 'bold'),
                 bg='#A6F3FE').grid(row=2, column=0, padx=(5, 2), pady=5, sticky='nsew')

        self.selected_market_2 = tk.StringVar()
        self.selected_market_2.set('Market2')

        dropdown_markets_2 = tk.OptionMenu(markets_frame, self.selected_market_2, *options)
        dropdown_markets_2.config(width=10)
        dropdown_markets_2.config(bg='#A6F3FE', activebackground='#90E9F7', borderwidth=2, relief=tk.RAISED, highlightthickness=0,
                                  font=('Helvetica', '10', 'italic bold'))
        dropdown_markets_2['menu'].config(bg='#90E9F7', font=('Helvetica', '10', 'italic bold'))
        dropdown_markets_2.grid(row=2, column=1, padx=(2, 5), pady=(5, 5), sticky='nsew')

        markets_frame.grid(row=1, column=3, columnspan=2, rowspan=4, padx=(0, 10), pady=(0, 4), sticky='nsew')


        notif_interval_frame = tk.Frame(self, relief=tk.GROOVE, bg='#A6F3FE', borderwidth=4)

        notif_label_frame = tk.Frame(notif_interval_frame, bg='#A6F3FE')
        tk.Label(notif_label_frame, text='Seconds Between Same Notification:', font=('Helvetica', '11', 'bold'),
                 bg='#A6F3FE').grid(row=0, column=0, padx=(10, 5), pady=0, ipady=0, sticky='sew')
        tk.Label(notif_label_frame, text='(for not notifying the same situation over and over)', font=('Helvetica', '8', 'italic'),
                 bg='#A6F3FE').grid(row=1, column=0, padx=(10, 5), pady=0, ipady=0, sticky='new')
        notif_label_frame.grid(row=1, column=0, rowspan=2, padx=(0, 30), pady=4, sticky='nsew')

        self.notif_interval_variable = tk.IntVar()
        interval_scale = tk.Scale(notif_interval_frame, variable=self.notif_interval_variable, from_=15, to=300, highlightcolor='white',
                                  bg='#A6F3FE', highlightbackground='#A6F3FE', activebackground='#A6F3FE', troughcolor='#70C9D7', 
                                  orient=tk.HORIZONTAL)
        interval_scale.bind('<ButtonRelease-1>', lambda *args: self.commands.append(f'self.controller.backend_application.set_required_alert_interval({self.notif_interval_variable.get()})'))
        interval_scale.bind('<ButtonRelease-2>', lambda *args: self.commands.append(f'self.controller.backend_application.set_required_alert_interval({self.notif_interval_variable.get()})'))
        interval_scale.bind('<ButtonRelease-3>', lambda *args: self.commands.append(f'self.controller.backend_application.set_required_alert_interval({self.notif_interval_variable.get()})'))
        interval_scale.grid(row=0, column=1, rowspan=2, padx=(5, 10), pady=(0, 4), sticky='nsew')
        

        notif_interval_frame.grid(row=5, column=0, columnspan=5, rowspan=2, padx=10, pady=(0, 5), sticky='nsew')


    def refresh_data(self):
        backend = self.controller.backend_application
        tmp_market1, tmp_market2 = backend.market_names
        self.tmp_alerts = backend.alerts.copy()
        tmp_required_alert_interval = backend.required_alert_interval

        self.selected_market_1.set(tmp_market1)
        self.selected_market_2.set(tmp_market2)
        self.notif_interval_variable.set(tmp_required_alert_interval)
        self.alerts_listbox.delete(0, tk.END)
        for alert in self.tmp_alerts:
            self.alerts_listbox.insert(tk.END, alert)


    def add_alert(self):
        # open a popup and then take the value for alert with enrtry and close it and then 
        #  add to the self.commands and alerts_listbox
        pop = Popup(self)
        self.wait_window(pop)
        new_alert = pop.alert_value
        if new_alert not in self.tmp_alerts and new_alert != None:
            self.commands.append(f'self.controller.backend_application.add_alert({new_alert})')
            alert_index = 0
            for alert in self.tmp_alerts:
                if alert > new_alert:
                    break
                alert_index += 1
            self.alerts_listbox.insert(alert_index, new_alert)
            self.tmp_alerts.insert(alert_index, new_alert)


    def remove_selected_alerts(self):
        selected_alerts = sorted(self.alerts_listbox.curselection(), reverse=True)
        # reverse=True is for not changing indexes for further indexes while removing the top ones
        sorted_all_alerts = sorted(self.tmp_alerts)
        for alert_index in selected_alerts:
            alert = sorted_all_alerts[alert_index]
            self.commands.append(f'self.controller.backend_application.remove_alert({alert})')
            self.alerts_listbox.delete(alert_index)

    def cancel_settings(self):
        self.commands.clear()
        self.controller.show_main_page()

    def set_markets(self):
        backend = self.controller.backend_application
        market1_name = self.selected_market_1.get()
        market2_name = self.selected_market_2.get()
        if (market1_name, market2_name) != backend.market_names and market1_name != market2_name:
            self.controller.set_markets(market1_name, market2_name)

    def save_settings(self):
        print(self.commands)
        for command in self.commands:
            exec(command)
        self.commands.clear()

        self.set_markets()
        
        self.controller.show_main_page()

    @property
    def id(self):
        return self.__ID

    def __str__(self):
        return self.__ID


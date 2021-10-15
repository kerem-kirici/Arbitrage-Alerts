import tkinter as tk


class MainPage(tk.Frame):

    __ID = 'MainPage'

    def __init__(self, parent, controller):
        super().__init__(parent, bg='#A6F3FE')

        self.controller = controller
        self.market1_name = None
        self.market2_name = None

        tk.Label(self, text='Arbitrage', font=('Helvetica', '14', 'italic'),
                 bg='#A6F3FE').grid(row=0, column=0, padx=10, pady=4, sticky='w')


        tk.Button(self, text='Settings', font=('Calibri', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.show_settings_page).grid(row=0, column=4, sticky='ew', padx=10, pady=4)


        # Date-Time and USD/TRY content
        first_row = tk.Frame(self, relief=tk.GROOVE, borderwidth=5, bg='#A6F3FE')

        self.datetime_label = tk.Label(first_row, text='00/00/0000, 00:00:00', font=('Helvetica', '11'), bg='#A6F3FE')
        self.datetime_label.grid(row=0, column=0, columnspan=8, padx=(10, 180), pady=10, sticky='w')

        usdtry_name_label = tk.Label(first_row, text='USDTRY:', font=('Helvetica', '11', 'italic'), fg='red', bg='#A6F3FE')
        usdtry_name_label.grid(row=0, column=8, padx=0, pady=10, sticky='e')

        self.usdtry_value_label = tk.Label(first_row, text='0.000', font=('Helvetica', '11', 'bold italic'), fg='red', bg='#A6F3FE')
        self.usdtry_value_label.grid(row=0, column=9, padx=(0, 10), pady=10, sticky='w')

        first_row.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 4), sticky='we')


        # USDT/TRY price table content
        price_table = tk.Frame(self, relief=tk.GROOVE, borderwidth=5, bg='#A6F3FE')

        latest_price_label = tk.Label(price_table, text='Latest Price', font=('Times', '11', 'bold'), bg='#A6F3FE')
        bid_price_label = tk.Label(price_table, text='Bid Price', font=('Times', '11', 'bold'), bg='#A6F3FE')
        ask_price_label = tk.Label(price_table, text='Ask Price', font=('Times', '11', 'bold'), bg='#A6F3FE')
        latest_price_label.grid(row=0, column=1, padx=18, pady=(8, 2), sticky='nsew')
        bid_price_label.grid(row=0, column=2, padx=18, pady=(8, 2), sticky='nsew')
        ask_price_label.grid(row=0, column=3, padx=18, pady=(8, 2), sticky='nsew')

        self.market1_name_label = tk.Label(price_table, text='Market1', font=('Times', '12', 'bold'), bg='#A6F3FE')
        self.market2_name_label = tk.Label(price_table, text='Market2', font=('Times', '12', 'bold'), bg='#A6F3FE')
        difference_name_label = tk.Label(price_table, text='Difference', font=('Times', '12', 'bold'), bg='#A6F3FE')
        self.market1_name_label.grid(row=1, column=0, padx=(5, 20), pady=(0, 5), sticky='nse')
        self.market2_name_label.grid(row=2, column=0, padx=(5, 20), pady=(0, 5), sticky='nse')
        difference_name_label.grid(row=3, column=0, padx=(5, 20), pady=(0, 5), sticky='nse')
        self.market1_price_label_latest = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.market1_price_label_bid = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.market1_price_label_ask = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.market2_price_label_latest = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.market2_price_label_bid = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.market2_price_label_ask = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.difference_label_latest = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.difference_label_bid = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')
        self.difference_label_ask = tk.Label(price_table, text='0.000', font=('Helvetica', '12', 'bold'), fg='dark blue', bg='#A6F3FE')

        self.market1_price_label_latest.grid(row=1, column=1, padx=18, pady=(0, 5), sticky='nsew')
        self.market1_price_label_bid.grid(row=1, column=2, padx=18, pady=(0, 5), sticky='nsew')
        self.market1_price_label_ask.grid(row=1, column=3, padx=18, pady=(0, 5), sticky='nsew')
        self.market2_price_label_latest.grid(row=2, column=1, padx=18, pady=(0, 5), sticky='nsew')
        self.market2_price_label_bid.grid(row=2, column=2, padx=18, pady=(0, 5), sticky='nsew')
        self.market2_price_label_ask.grid(row=2, column=3, padx=18, pady=(0, 5), sticky='nsew')
        self.difference_label_latest.grid(row=3, column=1, padx=18, pady=(0, 5), sticky='nsew')
        self.difference_label_bid.grid(row=3, column=2, padx=18, pady=(0, 5), sticky='nsew')
        self.difference_label_ask.grid(row=3, column=3, padx=18, pady=(0, 5), sticky='nsew')

        price_table.grid(row=2, column=0, columnspan=5, rowspan=4, padx=10, pady=(0, 5), sticky='we')


        tk.Button(self, text='Notifications', font=('Calibri', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.show_notif_page).grid(row=6, column=0, sticky='ew', padx=10, pady=(0, 4))

        tk.Button(self, text='Exit', font=('Calibri', '12'), bg='#A6F3FE', activebackground='#90E9F7',
                  command=self.controller.destroy).grid(row=6, column=4, sticky='ew', padx=10, pady=(0, 4))

    def refresh_data(self):
        backend = self.controller.backend_application
        self.datetime_label.config(text=backend.last_refresh_date)
        self.usdtry_value_label.config(text=backend.UsdTry_Price)

        (market1_name, market2_name) = backend.market_names

        if self.market1_name != market1_name:
            self.market1_name_label.config(text=market1_name)
            self.market1_name = market1_name

        if self.market2_name != market2_name:
            self.market2_name_label.config(text=market2_name)
            self.market2_name = market2_name

        price_table_data = backend.price_table

        self.market1_price_label_latest.config(text=price_table_data['Latest Price'][market1_name])
        self.market1_price_label_bid.config(text=price_table_data['Bid Price'][market1_name])
        self.market1_price_label_ask.config(text=price_table_data['Ask Price'][market1_name])

        self.market2_price_label_latest.config(text=price_table_data['Latest Price'][market2_name])
        self.market2_price_label_bid.config(text=price_table_data['Bid Price'][market2_name])
        self.market2_price_label_ask.config(text=price_table_data['Ask Price'][market2_name])

        self.difference_label_latest.config(text=price_table_data['Latest Price']['Difference'])
        self.difference_label_bid.config(text=price_table_data['Bid Price']['Difference'])
        self.difference_label_ask.config(text=price_table_data['Ask Price']['Difference'])

    @property
    def id(self):
        return self.__ID
    
    def __str__(self):
        return self.__ID


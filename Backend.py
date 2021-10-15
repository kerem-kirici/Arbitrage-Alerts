from Webscraper import Driver, TrBinanceScraper, BtcTurkScraper, UsdScraper
import os
import json
from datetime import datetime
import time
from playsound import playsound
from gtts import gTTS
from collections import defaultdict
import pandas as pd
import numpy as np



class Backend:

    # Defaut Values
    _DEFAULT_ALERT_BOUNDS = []
    _DEFAULT_market1 = TrBinanceScraper.id_name
    _DEFAULT_market2 = BtcTurkScraper.id_name
    _DEFAULT_REQUIRED_ALERT_INTERVAL = 60 

    # Class Variables
    _ALERT_BOUNDS = []
    _REQUIRED_ALERT_INTERVAL = None 


    _SOUNDS_FILE = ".\\sounds"
    _MARKET_OPTIONS = [TrBinanceScraper, BtcTurkScraper]


    def __init__(self, headless):

        # setup
        self.headless = headless
        self._driver = None
        self._market1 = None
        self._market2 = None
        self._usdmarket = None

        self._refreshed = False
        self._last_refresh_date = None

        # set((notif1, datetime1), (notif2, datetime2), ...)
        self.__notifications = set()

        # Pandas DataFrame for all price data
        self.__price_table = None

        self.__UsdTry_Price = None


        self.__ALERT_TIMES = defaultdict(int)
        # ALERT_TIMES: 

        # Because it is a defaultdict, we don't realy need to assign values at first for all alert possibilities,
        #  if there is no member for that alert in the ALERT_TIMES it will return 0 as we would with a normal dict


        self.__LAST_ALERT = None
        # LAST_ALERT: 

        #         (      lower bound ,   upper bound    )
        #         (          0       , ALERT_BOUNDS[0]  )
        #         (  ALERT_BOUNDS[0] , ALERT_BOUNDS[1]  )
        #         (  ALERT_BOUNDS[1] , ALERT_BOUNDS[2]  )
        #         (      ...         ,      ...         )
        #         ( ALERT_BOUNDS[-1] ,   float("inf")   )


        if not os.path.isdir(Backend._SOUNDS_FILE):
            os.mkdir(Backend._SOUNDS_FILE)

        self.__reset_scrapers()
        self.__set_settings()

    @property
    def price_table(self):
        return self.__price_table

    @property
    def UsdTry_Price(self):
        return self.__UsdTry_Price
    
    @property
    def last_refresh_date(self):
        return self._last_refresh_date

    @property
    def market_names(self):
        return (self._market1.name, self._market2.name)

    @property
    def notifications(self):
        return self.__notifications

    @property
    def alerts(self):
        return self._ALERT_BOUNDS

    @property
    def required_alert_interval(self):
        return self._REQUIRED_ALERT_INTERVAL

    @property
    def market_options(self):
        return [option.name for option in self._MARKET_OPTIONS]

    @property
    def market_name_id_table(self):
        return dict((option.name, option.id_name) for option in self._MARKET_OPTIONS)
    

    def remove_notification(self, notification):
        self.__notifications.remove(notification)    

    def close(self):
        self._driver.quit()

    def __reset_scrapers(self):
        if self._driver != None:
            self._driver.quit()
        self._driver = Driver(self.headless)
        self._market1 = None
        self._market2 = None
        self._usdmarket = UsdScraper(self._driver)

    def refresh(self):

        self._market1.refresh()
        self._market2.refresh()
        self._usdmarket.refresh()

        self._refreshed = all((self._market1.refreshed, self._market2.refreshed, self._usdmarket.refreshed))

        if self._refreshed:
            self._last_refresh_date = self.get_datetime_str()

            self._market1.refresh_prices()
            self._market2.refresh_prices()
            self._usdmarket.refresh_prices()

            market1_prices = self._market1.get_prices()
            market2_prices = self._market2.get_prices()
            arithmatic_mean = abs(sum(market1_prices) - sum(market2_prices))/3

            higher_market_name = self._market1.name if sum(market1_prices) >= sum(market2_prices) else self._market2.name

            if len(self._ALERT_BOUNDS):

                if arithmatic_mean < self._ALERT_BOUNDS[0]:
                    possible_alert_gap = (0, self._ALERT_BOUNDS[0])
                    if self.__LAST_ALERT != possible_alert_gap and time.time() - self.__ALERT_TIMES[possible_alert_gap] > self._REQUIRED_ALERT_INTERVAL:
                        self.__LAST_ALERT = possible_alert_gap
                        self.__ALERT_TIMES[possible_alert_gap] = int(time.time())
                        self.__send_alert(higher_market_name)

                for i in range(len(self._ALERT_BOUNDS)-1):

                    if self._ALERT_BOUNDS[i] <= arithmatic_mean < self._ALERT_BOUNDS[i+1]:

                        possible_alert_gap = (self._ALERT_BOUNDS[i], self._ALERT_BOUNDS[i+1])
                        if self.__LAST_ALERT != possible_alert_gap and time.time() - self.__ALERT_TIMES[possible_alert_gap] > self._REQUIRED_ALERT_INTERVAL:
                            self.__LAST_ALERT = possible_alert_gap
                            self.__ALERT_TIMES[possible_alert_gap] = int(time.time())
                            self.__send_alert(higher_market_name)

                if self._ALERT_BOUNDS[-1] <= arithmatic_mean:
                    possible_alert_gap = (self._ALERT_BOUNDS[-1], float('inf'))
                    if self.__LAST_ALERT != possible_alert_gap and time.time() - self.__ALERT_TIMES[possible_alert_gap] > self._REQUIRED_ALERT_INTERVAL:
                        self.__LAST_ALERT = possible_alert_gap
                        self.__ALERT_TIMES[possible_alert_gap] = int(time.time())
                        self.__send_alert(higher_market_name)


            f_formater = lambda x: "{:.3f}".format(x)

            prices_array = np.array([[f_formater(self._market1.latest_price),
                                      f_formater(self._market1.bid_price), 
                                      f_formater(self._market1.ask_price)
                                      ], 

                                     [f_formater(self._market2.latest_price), 
                                      f_formater(self._market2.bid_price), 
                                      f_formater(self._market2.ask_price)
                                      ], 

                                     [
                                      f_formater(self._market1.latest_price - self._market2.latest_price),
                                      f_formater(self._market1.bid_price - self._market2.bid_price),
                                      f_formater(self._market1.ask_price - self._market2.ask_price)
                                      ]
                                    ])

            self.__UsdTry_Price = f_formater(self._usdmarket.latest_price)

            self.__price_table = pd.DataFrame(prices_array, 
                                            index=[self._market1.name, self._market2.name, "Difference"],
                                            columns=['Latest Price', 'Bid Price', 'Ask Price'])

    def __send_alert(self, higher_market_name):

        (lower_price, higher_price) = self.__LAST_ALERT

        speech_text = "Difference"

        #speech_text
        if higher_price == float("inf"):
            speech_text += " came to {:.1f} cents and higher".format(lower_price*100)
        else:
            speech_text += " came between {:.1f} and {:.1f} cents".format(lower_price*100, higher_price*100)
        speech_text += f" for {higher_market_name}"

        # notification_text
        if higher_price == float("inf"):
            notification_text = "Difference is more than {:.1f} cents - {}".format(lower_price*100, higher_market_name)
        else:
            notification_text = "Difference is less than {:.1f} cents - {}".format(higher_price*100, higher_market_name)

        self.__notifications.add((notification_text, self.get_datetime()))

        # file_name
        if higher_price ==float("inf"):
            file_name = f"Alert-{higher_market_name}-{int(lower_price*10**3)}-inf.mp3"
        else:
            file_name = f"Alert-{higher_market_name}-{int(lower_price*10**3)}-{int(higher_price*10**3)}.mp3"

        sound_file_path = os.path.join(Backend._SOUNDS_FILE, file_name)

        if not os.path.isfile(sound_file_path):
            obj = gTTS(text=speech_text, lang="en", slow=True)
            obj.save(sound_file_path)

        playsound(sound_file_path, False)

    def __set_settings(self):
        data = self.__import_settings()
        try: 
            self.__set_data(data)

        except Exception as e: 
            print(f"An Error Occured While Importing Settings Data: \n{e}\n\nReseting Settings..\n")
            if not self.__reset_settings():
                print("Both Importing Settings Data and Reseting Settings functions couln't handled")
                raise 
            else:
                print("Settings Successfully Reset.\n\n")
                data = self.__import_settings()
                self.__set_data(data)

    def __import_settings(self):
        try:
            with open("settings.json", "r") as read_file:
                data = json.load(read_file)
                read_file.close()
                
        except Exception as e:
            print(f"An Error Occured While Importing Settings File: \n{e}\n\nReseting Settings..\n")
            if not self.__reset_settings():
                print("Both Importing Settings and Reseting Settings functions couln't handled")
                raise 
            else:
                print("Settings Successfully Reset.\n\n")

                with open("settings.json", "r") as read_file:
                    data = json.load(read_file)
                    read_file.close()
                    
        return data

    def __set_data(self, data):
        self._ALERT_BOUNDS = data["AlertBounds"]

        for market in self._MARKET_OPTIONS:
            if market.id_name == data["Market1"]:
                self._market1 = market(driver = self._driver)
            if market.id_name == data["Market2"]:
                self._market2 = market(driver = self._driver)

        self._REQUIRED_ALERT_INTERVAL = data["RequiredAlertInterval"] 

    def __get_default_data(self):
        data = {
                "AlertBounds": Backend._DEFAULT_ALERT_BOUNDS,
                "Market1": Backend._DEFAULT_market1,
                "Market2": Backend._DEFAULT_market2,
                "RequiredAlertInterval": Backend._DEFAULT_REQUIRED_ALERT_INTERVAL
               }

        return data

    def __update_settings_element(self, element, value):
        data = self.__import_settings()
        data[element] = value
        self.__export_settings(data)

    def __reset_settings(self):
        data = self.__get_default_data()
        reset_successful = self.__export_settings(data)
        return reset_successful

    def __export_settings(self, data):
        try: 
            with open("settings.json", "w") as file:
                json.dump(data, file, indent=4)
                file.close()
            return True

        except Exception as e:
            print(f"An Error Occured While Exporting Settings File: \n{e}\n\n")
            return False

    def add_alert(self, alert):
        self._ALERT_BOUNDS.append(alert)
        self._ALERT_BOUNDS.sort()

        self.__update_settings_element("AlertBounds", self._ALERT_BOUNDS)

    def remove_alert(self, alert):
        self._ALERT_BOUNDS.remove(alert)

        self.__update_settings_element("AlertBounds", self._ALERT_BOUNDS)

    def set_markets(self, Market1_id, Market2_id):
        print("\nSetting new Markets. This may take a while..\n")
        self.__reset_scrapers()

        for market in self._MARKET_OPTIONS:
            if market.id_name == Market1_id:
                self._market1 = market(driver = self._driver)
            if market.id_name == Market2_id:
                self._market2 = market(driver = self._driver)

        self.__update_settings_element("Market1", self._market1.id_name)
        self.__update_settings_element("Market2", self._market2.id_name)

        print("\nNew Markets Set. Good luck in the Markets! We hope you earn the best.\n")

    def set_required_alert_interval(self, value):
        self._REQUIRED_ALERT_INTERVAL = value

        self.__update_settings_element("RequiredAlertInterval", self._REQUIRED_ALERT_INTERVAL)

    @staticmethod
    def get_datetime_str():
        return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def get_datetime():
        return datetime.now()

    def __repr__(self):
        return (f'Backend(AlertBounds={self._ALERT_BOUNDS}, Market1={repr(self._market1)}, '
                f'Market2={repr(self._market2)}, RequiredAlertInterval={self._REQUIRED_ALERT_INTERVAL}, '
                f'LastAlert={self.__LAST_ALERT}, AlertTimes={dict(self.__ALERT_TIMES)}, Notifications={self.__notifications})')



if __name__ == '__main__':
    b = Backend(False)
    print(repr(b), end="\n\n")

    b.add_alert(0.005)
    print(repr(b), end="\n\n")

    while True:

        b.refresh()
        print(b.get_datetime_str())
        print(b.price_table, end='\n\n')
        print(b.UsdTry_Price, end='\n\n')
        print(repr(b))

        time.sleep(1)

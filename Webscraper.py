from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Driver(webdriver.Chrome):

    def __init__(self, headless):
        options = Options()
        # this argument makes the driver to pass security checks
        options.add_argument("--disable-blink-features=AutomationControlled")

        # headless option of the driver
        options.headless = headless

        super().__init__('.\\driver\\chromedriver', options=options)


class Scraper:

    DELAY_SEC = 10

    def __init__(self, url, id_name, driver, bid_price_scraper, latest_price_scraper, ask_price_scraper):
        # the url we want to scrape
        self.url = url

        # functions to scrape the price data from the url
        self.bid_price_scraper = bid_price_scraper
        self.latest_price_scraper = latest_price_scraper
        self.ask_price_scraper = ask_price_scraper

        # this part helps us to use the same driver and 
        #  not opening more than one driver and switch between windows
        self.id_name = id_name
        self.__driver = driver

        self.__driver.execute_script(f"window.open('about:blank', '{id_name}');")
        self.__driver.switch_to.window(id_name)
        self.__driver.get(self.url)


        # waiting for the driver to open and load the page successfully
        time.sleep(Scraper.DELAY_SEC)

        # defining the class variables
        self.__page_source = None

        self.__latest_price = None
        self.__ask_price = None
        self.__bid_price = None
        self.__new_latest_price = None
        self.__new_ask_price = None
        self.__new_bid_price = None

        self.refreshed = True


    def get_prices(self):
        return (self.__latest_price, self.__bid_price, self.__ask_price)

    @property
    def latest_price(self):
        return self.__latest_price
    
    @property
    def bid_price(self):
        return self.__bid_price

    @property
    def ask_price(self):
        return self.__ask_price

    def refresh(self):
        
        # opening the page for specific window
        self.__driver.switch_to.window(self.id_name)
        self.__page_source = self.__driver.page_source


        # okay if you need explanation for this line,
        #  what are you looking for in this project??

        # Google: python webscraping
        soup = BeautifulSoup(self.__page_source, "html.parser")

        # theese lines looks for current prices 

        # BUT!!
        # if, by one chance, one of the prices cannot be refreshed, 
        #  then it does not refresh other prices too, 
        #  for not misleading the user by prices from different times.

        try:
            self.__new_ask_price = self.ask_price_scraper(soup)
        except:
            self.refreshed = False

        try:
            self.__new_latest_price = self.latest_price_scraper(soup)
        except:
            self.refreshed = False

        try:
            self.__new_bid_price = self.bid_price_scraper(soup)
        except:
            self.refreshed = False


    def refresh_prices(self):
        # this functions runs only if:
        #  all of the scrapers refreshed seccessfully
        self.__latest_price = self.__new_latest_price
        self.__bid_price = self.__new_bid_price
        self.__ask_price = self.__new_ask_price

    
# Subclasses of Scraper Class (For Specific urls)

# In theese Classes the Price Scraper functions are, 
#  written in lambda form but with a few HTML knowledge
#  everyone can figure all of them out. 

class TrBinanceScraper(Scraper):
    
    name = "Tr Binance"
    url = "https://www.trbinance.com/trade/USDT_TRY" 
    id_name = "trbinance"

    def __init__(self, driver):
        bid_price_scraper = lambda s: max([float(x.text) for x in s.find("div", class_="bids").find_all("span", class_="price rise")])
        latest_price_scraper = lambda s: float(s.find("div", class_="latest-price").find("span", class_="price rise").text)
        ask_price_scraper = lambda s: min([float(x.text) for x in s.find("div", class_="asks").find_all("span", class_="price fall")])

        super().__init__(url=self.url, id_name=self.id_name, driver=driver, bid_price_scraper=bid_price_scraper, latest_price_scraper=latest_price_scraper, ask_price_scraper=ask_price_scraper)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id_name


class BtcTurkScraper(Scraper):

    name = "BTC Turk"
    url = "https://pro.btcturk.com/en/pro/exchange/USDT_TRY"
    id_name = "btcturk"

    def __init__(self, driver):
        bid_price_scraper = lambda s: float(s.find("output", id="ex-advanced-ticker-bid").text.split()[0])
        latest_price_scraper = lambda s: float(s.find("output", id="ex-advanced-ticker-last").text.split()[0])
        ask_price_scraper = lambda s: float(s.find("output", id="ex-advanced-ticker-ask").text.split()[0])

        super().__init__(url=self.url, id_name=self.id_name, driver=driver, bid_price_scraper=bid_price_scraper, latest_price_scraper=latest_price_scraper, ask_price_scraper=ask_price_scraper)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id_name


class UsdScraper(Scraper):

    name = "USDTRY"
    url = "https://www.tradingview.com/symbols/USDTRY/"
    id_name = "usdtry"

    def __init__(self, driver):
        bid_price_scraper = lambda s: None
        latest_price_scraper = lambda s: float(s.find("div", class_="tv-symbol-price-quote__value js-symbol-last").text)
        ask_price_scraper = lambda s: None

        super().__init__(url=self.url, id_name=self.id_name, driver=driver, bid_price_scraper=bid_price_scraper, latest_price_scraper=latest_price_scraper, ask_price_scraper=ask_price_scraper)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id_name


if __name__ == '__main__':
    d = Driver(False)
    s1 = UsdScraper(d)
    s2 = BtcTurkScraper(d)
    s1.refresh()
    s1.refresh_prices()
    print(s1.refreshed, s1.get_prices())
    s2.refresh()
    s2.refresh_prices()
    print(s2.refreshed, s2.get_prices())
    
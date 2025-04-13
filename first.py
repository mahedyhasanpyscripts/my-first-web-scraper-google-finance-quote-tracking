import requests as rq 
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str 
    exchange: str 
    price: float = 0  
    currency: str = "USD"
    usd_price: float = 0

    def __post_init__(self):  
        price_info = get_price_info(self.ticker, self.exchange)
        self.price = price_info['price']
        self.currency = price_info['currency']
        self.usd_price = price_info['usd_price']




def convert_to_usd(currency):
    fx_url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = rq.get(fx_url)
    soup = BeautifulSoup(resp.content , "html.parser")
    fx_rate = soup.find("div",attrs={"data-last-price" : True})
    fx = float(fx_rate["data-last-price"])

    return fx


def get_price_info(ticker , exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = rq.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    price_div = soup.find("div",attrs={"data-last-price" : True})
    price = float(price_div['data-last-price'])
    currency = price_div['data-currency-code']

    usd_price = price 

    if(currency != "USD"):
        usd_price = round(price * convert_to_usd(currency),2)

    return {
        "ticker" : ticker,
        "price" : price , 
        "exchange" : exchange , 
        "currency" : currency,
        "usd_price" : usd_price
    }

if __name__ == "__main__":
    print(Stock("SHOP", "TSE"))
    print(Stock("SHOP","NASDAQ"))

    
    

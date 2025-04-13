import requests as rq 
from bs4 import BeautifulSoup

def get_price_info(ticker , exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = rq.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    price_div = soup.find("div",attrs={"data-last-price" : True})
    price = float(price_div['data-last-price'])
    currency = price_div['data-currency-code']
    return {
        "ticker" : ticker,
        "price" : price , 
        "exchange" : exchange , 
        "currency" : currency
    }J

if __name__ == "__main__":
    print(get_price_info("NVDA","NASDAQ"))
    

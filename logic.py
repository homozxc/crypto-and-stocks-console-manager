import json
import datetime
import yfinance

WATCHLIST = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "SOL-USD": "Solana",
    "XRP-USD": "XRP",
    "DOGE-USD": "Dogecoin",
    "AAPL": "Apple Inc.",
    "TSLA": "Tesla Inc.",
    "MSFT": "Microsoft Corp.",
    "AMZN": "Amazon.com",
    "NVDA": "NVIDIA Corp."
}

def get_real_price(ticker:str):
    '''
    Принимает на вход строку с названием тикера из словаря WATCHLIST5.

    Используя библиотеку yfinance, получает цену закрытия тикера за
    последний торговый день.

    Возвращает цену закрытия тикера в формате float. Если входная переменная содержит
    пустую строку или во время выполнения кода возникает ошибка, возвращает None

    :param: str ticker: название тикера из списка WATCHLIST
    :return: Цена тикера за последний торговый день if not data.empty else None
    :rtype: float

    :example:

    >>> 'BTC-USD'
    >>> get_real_price('BTC-USD')
    90000.00001
    '''

    print(f'Fetching the price of {ticker}...')
    try:
        data = yfinance.Ticker(ticker).history(period='1d')
        return data['Close'].iloc[-1] if not data.empty else None
    except:
        return None
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

def load_portfolio(filename:str):
    '''
    Получает название файла json, загружает файл. Если возникает ошибка при загрузке,
    то создает портфолио по умолчанию.

    :param str filename: название файла json, который загружается
    :return: Загруженный файл json
    '''
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {"cash": 0.0, "positions": {}, "history": []}

def save_portfolio(data, filename="portfolio.json"):
    '''
    Сохраняет словарь data, который содержит информацию о портфеле, в формате json

    :param dict data:
    :param str filename:
    :return:
    '''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def update_cash(data, amount):
    '''
    Получает на вход словарь, хранящий в себе информацию о портфолио,
    и сумму, которую нужно добавить или вычесть из счета.
    Прибавляет к элементу с ключом cash число amount.

    :param dict data:
    :param int or float amount:
    :return: Словарь с обновленным количеством денег на счете
    '''
    data["cash"] += amount
    log_action(data, f"Cash update: {amount}")
    return data

def buy_asset(data, ticker, qty):
    '''
    Принимает словарь data, содержащий всю информацию о портфеле,
    название тикера ticker из словаря WATCHLIST, количество акций qty,
    которое нужно приобрести.

    Если тикер есть в словаре WATCHLIST,
    то обращается к функции get_real_price и получает
     цену тикера. Если на счете достаточно денег, то обновляет
     в словаре data элемент с ключом 'positions' и возвращает True.

     Если тикера нет в списке разрешенных, не удалось получить цену тикера или
     на счете недостаточно денег, то выводит соответствующее сообщение и возвращает False.

    :param dict data:
    :param str ticker:
    :param int or float qty:
    :return: True
    '''
    if ticker not in WATCHLIST:
        print(f"Error: {ticker} is not in watchlist.")
        return False

    price = get_real_price(ticker)
    if price is None:
        print("Could not fetch price. Transaction aborted.")
        return False

    cost = qty * price
    if cost > data["cash"]:
        print(f"Error: Insufficient funds. Cost: ${cost:.2f}, Cash: ${data['cash']:.2f}")
        return False

    data["cash"] -= cost

    if ticker in data["positions"]:
        old_qty = data["positions"][ticker]["qty"]
        old_avg = data["positions"][ticker]["avg_price"]
        new_qty = old_qty + qty
        new_avg = ((old_qty * old_avg) + cost) / new_qty

        data["positions"][ticker]["qty"] = new_qty
        data["positions"][ticker]["avg_price"] = new_avg
    else:
        data["positions"][ticker] = {"qty": qty, "avg_price": price}

    log_action(data, f"Bought {qty} {ticker} @ {price:.2f}")
    print(f"Successfully bought {qty} {ticker} at ${price:.2f}")
    return True
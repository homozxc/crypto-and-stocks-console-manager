def load_portfolio(path):
    return 1
def get_price(asset):
    price = 0
    return price

def show_statistics():
    return 1
def add_asset(asset):
    return 1
def swap_asset(asset1, asset2):
    return 1
def get_graph(path):
    return 1

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

def sell_asset(data, ticker, qty):
    '''
    Принимает на вход словарь data, содержащий всю информацию о портфеле,
    название тикера ticker из словаря WATCHLIST, количество акций qty,
    которое нужно продать.

    Обращается к функции get_real_price и получает актуальную цену тикера.
    В словаре data обновляет элементы с ключами 'cash' и 'positions' (количество денег на счете
    и позиции в портфеле) и возвращает True.

    Если тикера нет в списке имеющихся в портфеле, количество для продажи больше, чем количество
    имеющихся, или не удалось получить цену тикера, то выводит соответствующее сообщение и возвращает False.

    :param data:
    :param ticker:
    :param qty:
    :return: True or False
    '''
    if ticker not in data["positions"] or data["positions"][ticker]["qty"] < qty:
        print("Error: Not enough position to sell.")
        return False

    price = get_real_price(ticker)
    if price is None:
        print("Could not fetch price. Transaction aborted.")
        return False

    revenue = qty * price
    data["cash"] += revenue
    data["positions"][ticker]["qty"] -= qty

    if data["positions"][ticker]["qty"] <= 0:
        del data["positions"][ticker]

    log_action(data, f"Sold {qty} {ticker} @ {price:.2f}")
    print(f"Successfully sold {qty} {ticker} at ${price:.2f}")
    return True

'''
'''
'''
'''
'''
'''

def get_current_stats(data):
    """Calculates total portfolio value with LIVE prices."""

    current_asset_value = 0.0
    total_cost_basis = 0.0

    print("\n--- Fetching current prices for holdings ---")
    for ticker, info in data["positions"].items():
        price = get_real_price(ticker)
        if price is None:
            price = info["avg_price"]  # Fallback
            print(f"Using saved price for {ticker} (fallback)")

        val = info["qty"] * price
        cost = info["qty"] * info["avg_price"]

        current_asset_value += val
        total_cost_basis += cost

        pnl = val - cost
        pnl_percent = (pnl / cost * 100) if cost > 0 else 0
        print(f"{ticker}: {info['qty']} units | Price: ${price:.2f} | Val: ${val:.2f} | PnL: {pnl_percent:.2f}%")

    return {
        "cash": data["cash"],
        "asset_value": current_asset_value,
        "total_value": data["cash"] + current_asset_value,
        "total_pnl": current_asset_value - total_cost_basis
    }


def log_action(data, message):
    data["history"].append({
        "date": str(datetime.datetime.now()),
        "action": message,
        "cash_snapshot": data["cash"]
    })


def export_chart_data(data):
    print("\n--- History Export ---")
    print("Date,Action,Cash")
    for entry in data["history"]:
        print(f"{entry['date']},{entry['action']},{entry['cash_snapshot']}")
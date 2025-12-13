import json
import datetime
import yfinance
import matplotlib.pyplot as plt

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
    """
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
    """

    print(f'Узнаем цену {ticker}...')
    try:
        data = yfinance.Ticker(ticker).history(period='1d')
        return data['Close'].iloc[-1] if not data.empty else None
    except:
        return None

def load_portfolio(filename:str):
    """
    Получает название файла json, загружает файл. Если возникает ошибка при загрузке,
    то создает портфолио по умолчанию.

    :param str filename: название файла json, который загружается
    :return: Загруженный файл json
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {"cash": 1000, "positions": {}, "history": {}}

def save_portfolio(data, filename="portfolio.json"):
    """
    Сохраняет словарь data, который содержит информацию о портфеле, в формате json

    :param dict data:
    :param str filename:
    :return:
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def update_cash(data, amount):
    """
    Получает на вход словарь, хранящий в себе информацию о портфолио,
    и сумму, которую нужно добавить или вычесть из счета.
    Прибавляет к элементу с ключом cash число amount.

    :param dict data:
    :param int or float amount:
    :return: Словарь с обновленным количеством денег на счете
    """
    if 'cash' not in data or not isinstance(amount, (int, float)):
        return None
    data["cash"] += amount
    log_action(data, f"Обновление денег на счете: {amount}")
    return data

def buy_asset(data, ticker, qty):
    """
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
    """
    if qty <= 0:
        raise ValueError
    if ticker not in WATCHLIST:
        print(f"Ошибка: {ticker} нет в списке разрешенных акций и криптовалют.")
        return False

    price = get_real_price(ticker)
    if price is None:
        print("Не можем найти цену. Транзакция отклонена")
        return False

    cost = qty * price
    if cost > data["cash"]:
        print(f"Ошибка: Не хватает средств. Стоимость: ${cost:.2f}, Деньги на счету: ${data['cash']:.2f}")
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

    log_action(data, f"Купили {qty} {ticker} @ {price:.2f}")
    print(f"Успешно купили {qty} {ticker} по цене ${price:.2f}")
    return True

def sell_asset(data, ticker, qty):
    """
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
    """
    if qty <= 0:
        raise ValueError
    if ticker not in data["positions"] or data["positions"][ticker]["qty"] < qty:
        print("Ошибка: Нет такого кол-ва, чтобы продать.")
        return False

    price = get_real_price(ticker)
    if price is None:
        print("Не можем найти цену. Транзакция не прошла")
        return False

    revenue = qty * price
    data["cash"] += revenue
    data["positions"][ticker]["qty"] -= qty

    if data["positions"][ticker]["qty"] <= 0:
        del data["positions"][ticker]

    log_action(data, f"Продано {qty} {ticker} @ {price:.2f}")
    print(f"Успешно продано {qty} {ticker} at ${price:.2f}")
    return True


def export_history_data(data):
    """

    Выводит какие действия производились на кошельке

    :param dict data: Информация о кошельке

    :example:

    >>>a = {"cash":1000, "history": {"date":"2025-11-29 20:55:48.060410", "action":"Обновление счета: 10000.0", "cash_snapshot":10000.0}}
    >>>export_history_data(a)
    --- История портфеля ---
    Дата, Действие, Деньги
    2025-11-29 20:55:48.060410, Обновление счета: 10000.0, 10000.0

    """
    print("\n--- История портфеля ---")
    print("Дата, Действие, Деньги")
    for entry in data["history"]:
        print(f"{entry['date']}, {entry['action']}, {entry['cash_snapshot']}")


def get_chart(ticker, days):
    """

    Выводит график акции или криптовалюты за выбранное кол-во дней от сегодняшней даты

    :param str ticker: Тикер криптовалюты или акции
    :param days: В каком диапазоне дней будет график

    :example:
    >>>a="AAPL"
    >>>b=20
    >>>get_chart(a, b)
    chart of Apple Inc.
    """

    if ticker not in WATCHLIST:
        raise ValueError(f"Ошибка: {ticker} нет в списке разрешенных акций и криптовалют.")
    if days <= 0 or days > 10000:
        raise ValueError("Количество дней должно быть от 1 до 10000")

    print("загружаем график...")
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    df = yfinance.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False
    )
    df = df.stack(level="Ticker", future_stack=True)
    df.index.names = ["Date", "Symbol"]
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df = df.swaplevel(0, 1)
    df = df.sort_index()

    plt.figure(figsize=(10, 6))
    plt.grid(alpha=0.5)

    plt.plot(
        df.xs(ticker).index,
        df.xs(ticker)["Close"],
        color="blue",
        linewidth=1.5
    )

    plt.title(f"{ticker}")
    plt.xlabel("Дата")
    plt.ylabel("Цена ($)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def log_action(data, message):
    """

    Загружает действия в информацию о портфеле

    :param dict data: Информация о портфеле
    :param str message: Описываем какое действие сделали

    :example:
    >>>a={"cash":{"positions":{}}, "history":{}}
    >>>b="Bought"
    >>>log_action(a, b)
    """

    data["history"].append({
        "date": str(datetime.datetime.now()),
        "action": message,
        "cash_snapshot": data["cash"]
    })


def get_current_stats(data):
    """

    Считаем стоимость портфеля в реальном времени и показывает pnl

    :param dict data: Информации о портфеле
    :return: статистику о портфеле
    :rtype: dict

    :example:
    >>>a={"cash":1000,"positions":{"AAPL":{"qty":2, "avg_price":230}}, "history":}
    >>>get_current_stats(a)
    --- Ищем цену акций и крипты в портфеле ---
    AAPL: кол-во 2 | Цена: $250.00 | Стоимость: $500.00 | Изменение стоимости: 8.69%
    {
        "cash": 1000
        "assets_value": 500
        "total_value": 1500
        "total_pnl": 8.69%
    }
    """
    total_value = 0.0
    total_cost = 0.0

    print("\n--- Ищем цену акций и крипты в портфеле ---")
    for ticker, info in data["positions"].items():
        price = get_real_price(ticker)

        if price is None:
            price = info["avg_price"]
            print(f"Использую сохраненную цену {ticker}")

        current_asset_value = info["qty"] * price
        asset_cost = info["qty"] * info["avg_price"]
        total_value += current_asset_value
        total_cost += asset_cost

        pnl = current_asset_value - asset_cost
        pnl_percent = (pnl / asset_cost * 100) if asset_cost > 0 else 0
        print(f"{ticker}: кол-во {info['qty']} | Цена: ${price:.2f} | Стоимость: ${current_asset_value:.2f} | Изменение стоимости: {pnl_percent:.2f}%")

    return {
        "cash": data["cash"],
        "assets_value": total_value,
        "total_value": data["cash"] + total_value,
        "total_pnl": total_value - total_cost
    }

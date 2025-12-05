import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt


def export_history_data(data):
    print("\n--- History Export ---")
    print("Date,Action,Cash")
    for entry in data["history"]:
        print(f"{entry['date']},{entry['action']},{entry['cash_snapshot']}")


def get_chart(ticker, days):
    print("loading chart...")
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=days)
    df = yf.download(
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
    plt.xlabel("Date")
    plt.ylabel("Price ($)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def log_action(data, message):
    data["history"].append({
        "date": str(dt.datetime.now()),
        "action": message,
        "cash_snapshot": data["cash"]
    })


def get_current_stats(data):
    """

    Calculates total portfolio value with LIVE prices

    :param dict data: portfolio data
    :return: dictionary with statistics
    :rtype: dict

    :example:

    """
    current_asset_value = 0.0
    total_cost_basis = 0.0

    print("\n--- Fetching current prices for holdings ---")
    for ticker, info in data["positions"].items():
        price = get_real_price(ticker)

        if price is None:
            price = info["avg_price"]
            print(f"Using saved price for {ticker}")

        current_asset_value = info["qty"] * price
        total_cost_basis = info["qty"] * info["avg_price"]

        pnl = current_asset_value - total_cost_basis
        pnl_percent = (pnl / total_cost_basis * 100) if total_cost_basis > 0 else 0
        print(f"{ticker}: {info['qty']} units | Price: ${price:.2f} | Val: ${current_asset_value:.2f} | PnL: {pnl_percent:.2f}%")

    return {
        "cash": data["cash"],
        "asset_value": current_asset_value,
        "total_value": data["cash"] + current_asset_value,
        "total_pnl": current_asset_value - total_cost_basis
    }

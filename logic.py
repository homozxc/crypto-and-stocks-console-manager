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


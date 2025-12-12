import logic as l

FILENAME = "portfolio.json"

print("Хотите загрузить свой портфель или получить стартовый баланс?")
print("1. Загрузить портфель")
print("2. Получить стартовый баланс")
choice = input("\nВведите число: ")
if choice == '1':
    FILENAME = input("Введите имя файла: ")
portfolio = l.load_portfolio(FILENAME)


while True:
    print("\n=================================")
    print("   PYTHON PORTFOLIO MANAGER      ")
    print("=================================")

    print(f"Баланс : ${portfolio['cash']:.2f}")

    print("\n--- Доступные акции и криптовалюты ---")
    for t, n in l.WATCHLIST.items():
        print(f" {t:<10} : {n}")

    print("\n1. Добавление / Вывод средств")
    print("2. Купить")
    print("3. Продать")
    print("4. Статистика портфеля")
    print("5. Выгрузка истории транзакций")
    print("6. Показать график")
    print("7. Выход")

    choice = input("\nВведите число: ")

    if choice == '1':
        try:
            amt = float(input("Количество (+ чтобы ввести, - чтобы вывести): "))
            l.update_cash(portfolio, amt)
            l.save_portfolio(portfolio, FILENAME)
            print("Деньги обновлены.")
        except ValueError:
            print("Неверное значение.")

    elif choice == '2':
        print("Введите тикер из списка (BTC-USD, AAPL и т.д.)")
        ticker = input("Название: ").strip().upper()
        try:
            qty = float(input("Количество: "))
            if l.buy_asset(portfolio, ticker, qty):
                l.save_portfolio(portfolio, FILENAME)
        except ValueError:
            print("Неверное значение.")

    elif choice == '3':
        ticker = input("Тикер для продажи: ").strip().upper()
        try:
            qty = float(input("Количество: "))
            if l.sell_asset(portfolio, ticker, qty):
                l.save_portfolio(portfolio, FILENAME)
        except ValueError:
            print("Неверное значение.")

    elif choice == '4':
        stats = l.get_current_stats(portfolio)
        print("\n---------------------------------")
        print(f"Количество денег:    ${stats['cash']:.2f}")
        print(f"Ценность крипты и акций:  ${stats['assets_value']:.2f}")
        print(f"Общая ценность:  ${stats['total_value']:.2f}")
        print(f"Заработок/убыток:  ${stats['total_pnl']:.2f}")
        print("---------------------------------")

    elif choice == '5':
        l.export_history_data(portfolio)

    elif choice == '6':
        try:
            l.get_chart(input("Введите тикер: "), int(input("Введите кол-во дней: ")))
        except ValueError:
            print("Введено неверное значение")

    elif choice == "7":
        print("Сохраняем и выходим...")
        l.save_portfolio(portfolio, FILENAME)
        break
    else:
        print("Неверный вариант")

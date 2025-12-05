def export_history_data(data):
    print("\n--- History Export ---")
    print("Date,Action,Cash")
    for entry in data["history"]:
        print(f"{entry['date']},{entry['action']},{entry['cash_snapshot']}")

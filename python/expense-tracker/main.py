"""A tiny CSV-based command-line expense tracker."""

import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "amount", "note"]


def add_expense() -> None:
    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter an amount greater than zero.")
        return

    note = input("Note (optional): ").strip()
    new_file = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "category": category,
            "amount": f"{amount:.2f}",
            "note": note,
        })
    print("Expense saved.")


def show_summary() -> None:
    if not DATA_FILE.exists():
        print("No expenses recorded yet.")
        return

    total = 0.0
    print("\nDate        Category             Amount")
    print("-" * 44)
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            amount = float(row["amount"])
            total += amount
            print(f'{row["date"]:<12}{row["category"]:<21}{amount:>8.2f}')
    print("-" * 44)
    print(f"Total: {total:.2f}")


def main() -> None:
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses and total")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Choose 1, 2 or 3.")


if __name__ == "__main__":
    main()

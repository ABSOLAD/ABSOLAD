# Expense Tracker

A desktop expense tracker built with Python, Tkinter and SQLite.

## Features

- Add expenses with category, amount and optional note.
- View saved expenses in a table.
- Calculate total spending.
- Store data locally in `expenses.db`.
- Parameterized SQL queries and basic input validation.

## Run

```bash
python main.py
```

Requires Python 3.8+ with Tkinter. SQLite is included with standard Python builds; no pip packages are needed.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests use a temporary database and do not modify your personal expense data.

## Data and privacy

The database is created beside the application. Keep `expenses.db` private because it may contain personal spending information. Back it up before moving or deleting the project.

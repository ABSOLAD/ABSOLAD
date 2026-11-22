"""SQLite persistence for the expense tracker."""

import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

DEFAULT_DB = Path(__file__).with_name("expenses.db")


def connect(db_path: Optional[Path] = None) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path or DEFAULT_DB))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Optional[Path] = None) -> None:
    with connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                note TEXT NOT NULL DEFAULT ''
            )
        """)


def add_expense(category: str, amount: float, note: str = "",
                db_path: Optional[Path] = None) -> int:
    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    initialize_database(db_path)
    with connect(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO expenses(date, category, amount, note) VALUES (?, ?, ?, ?)",
            (date.today().isoformat(), category, round(float(amount), 2), note.strip()),
        )
        return int(cursor.lastrowid)


def get_expenses(db_path: Optional[Path] = None) -> list[dict]:
    initialize_database(db_path)
    with connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, date, category, amount, note FROM expenses ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_total(db_path: Optional[Path] = None) -> float:
    initialize_database(db_path)
    with connect(db_path) as connection:
        total = connection.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        return round(float(total), 2)

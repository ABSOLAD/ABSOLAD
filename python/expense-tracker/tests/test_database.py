import tempfile
import unittest
from pathlib import Path

from database import add_expense, get_expenses, get_total, initialize_database


class ExpenseDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test-expenses.db"
        initialize_database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_expense(self):
        add_expense("Food", 125.50, "Lunch", self.db_path)
        rows = get_expenses(self.db_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["category"], "Food")
        self.assertEqual(rows[0]["amount"], 125.5)

    def test_total_is_calculated(self):
        add_expense("Food", 100, db_path=self.db_path)
        add_expense("Travel", 50.25, db_path=self.db_path)
        self.assertEqual(get_total(self.db_path), 150.25)

    def test_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Food", 0, db_path=self.db_path)

    def test_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            add_expense("  ", 10, db_path=self.db_path)


if __name__ == "__main__":
    unittest.main()

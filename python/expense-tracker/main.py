"""Tkinter expense tracker backed by a local SQLite database."""

import tkinter as tk
from tkinter import messagebox, ttk
from database import add_expense, get_expenses, get_total, initialize_database


class ExpenseTracker:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("ABSOLAD | Expense Tracker")
        root.geometry("760x540")
        root.configure(bg="#111827")

        tk.Label(root, text="EXPENSE TRACKER", font=("Segoe UI", 20, "bold"),
                 bg="#111827", fg="#f9fafb").pack(pady=(20, 4))
        tk.Label(root, text="Your spending, organised.", font=("Segoe UI", 10),
                 bg="#111827", fg="#9ca3af").pack(pady=(0, 18))

        form = tk.Frame(root, bg="#1f2937", padx=16, pady=14)
        form.pack(fill="x", padx=22)
        self.category = tk.StringVar()
        self.amount = tk.StringVar()
        self.note = tk.StringVar()

        for label, variable, width in [
            ("Category", self.category, 20),
            ("Amount", self.amount, 12),
            ("Note", self.note, 25),
        ]:
            tk.Label(form, text=label, bg="#1f2937", fg="#e5e7eb").pack(
                side="left", padx=(0, 5))
            tk.Entry(form, textvariable=variable, width=width, bg="#374151",
                     fg="white", insertbackground="white", relief="flat").pack(
                side="left", padx=(0, 12), ipady=6)

        tk.Button(form, text="Add expense", command=self.add,
                  bg="#2563eb", fg="white", relief="flat",
                  padx=12, pady=7).pack(side="left")

        columns = ("date", "category", "amount", "note")
        self.table = ttk.Treeview(root, columns=columns, show="headings", height=13)
        for column, heading, width in [
            ("date", "DATE", 130), ("category", "CATEGORY", 180),
            ("amount", "AMOUNT", 110), ("note", "NOTE", 280),
        ]:
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, anchor="w")
        self.table.pack(fill="both", expand=True, padx=22, pady=18)

        self.total_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"),
                                    bg="#111827", fg="#34d399")
        self.total_label.pack(pady=(0, 18))
        self.refresh()

    def add(self) -> None:
        category = self.category.get().strip()
        try:
            amount = float(self.amount.get())
            if not category or amount <= 0:
                raise ValueError
            add_expense(category, amount, self.note.get().strip())
        except ValueError:
            messagebox.showerror("Invalid expense",
                                 "Enter a category and an amount greater than zero.")
            return
        self.category.set("")
        self.amount.set("")
        self.note.set("")
        self.refresh()

    def refresh(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        for row in get_expenses():
            self.table.insert("", "end", values=(
                row["date"], row["category"], f'{row["amount"]:.2f}', row["note"]))
        self.total_label.config(text=f"TOTAL SPENDING  |  {get_total():.2f}")


if __name__ == "__main__":
    initialize_database()
    app = tk.Tk()
    ExpenseTracker(app)
    app.mainloop()

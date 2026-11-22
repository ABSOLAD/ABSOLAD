"""Tkinter desktop interface for the password generator."""

import secrets
import string
import tkinter as tk
from tkinter import messagebox


def generate_password(length: int, use_upper: bool, use_lower: bool,
                      use_digits: bool, use_symbols: bool) -> str:
    """Return a password using the selected character groups."""
    groups = []
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append("!@#$%^&*()-_=+[]{};:,.?/")

    if not groups:
        raise ValueError("Select at least one character type.")
    if length < 8 or length > 128:
        raise ValueError("Length must be between 8 and 128.")

    # Include at least one character from every selected group.
    password = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    password.extend(secrets.choice(alphabet) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def main() -> None:
    root = tk.Tk()
    root.title("ABSOLAD | Password Generator")
    root.geometry("460x390")
    root.minsize(420, 360)
    root.configure(bg="#111827")

    title = tk.Label(root, text="PASSWORD GENERATOR", font=("Segoe UI", 17, "bold"),
                     fg="#f9fafb", bg="#111827")
    title.pack(pady=(24, 5))
    tk.Label(root, text="Generate a strong random password",
             font=("Segoe UI", 10), fg="#9ca3af", bg="#111827").pack(pady=(0, 20))

    length_var = tk.StringVar(value="16")
    result_var = tk.StringVar()
    options = {
        "Uppercase (A-Z)": tk.BooleanVar(value=True),
        "Lowercase (a-z)": tk.BooleanVar(value=True),
        "Numbers (0-9)": tk.BooleanVar(value=True),
        "Symbols (!@#)": tk.BooleanVar(value=True),
    }

    panel = tk.Frame(root, bg="#1f2937", padx=22, pady=18)
    panel.pack(fill="x", padx=28)
    tk.Label(panel, text="Password length (8–128)", fg="#e5e7eb",
             bg="#1f2937", font=("Segoe UI", 10, "bold")).pack(anchor="w")
    tk.Entry(panel, textvariable=length_var, font=("Segoe UI", 12),
             bg="#374151", fg="white", insertbackground="white",
             relief="flat").pack(fill="x", pady=(6, 12))

    for label, variable in options.items():
        tk.Checkbutton(panel, text=label, variable=variable, fg="#e5e7eb",
                       bg="#1f2937", activebackground="#1f2937",
                       activeforeground="white", selectcolor="#374151",
                       font=("Segoe UI", 10)).pack(anchor="w")

    result = tk.Entry(root, textvariable=result_var, justify="center",
                      font=("Consolas", 12), bg="#1f2937", fg="#34d399",
                      insertbackground="white", relief="flat")
    result.pack(fill="x", padx=28, pady=(18, 8))

    def create() -> None:
        try:
            result_var.set(generate_password(
                int(length_var.get()),
                options["Uppercase (A-Z)"].get(),
                options["Lowercase (a-z)"].get(),
                options["Numbers (0-9)"].get(),
                options["Symbols (!@#)"].get(),
            ))
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error))

    def copy() -> None:
        if result_var.get():
            root.clipboard_clear()
            root.clipboard_append(result_var.get())
            messagebox.showinfo("Copied", "Password copied to clipboard.")

    buttons = tk.Frame(root, bg="#111827")
    buttons.pack(pady=8)
    tk.Button(buttons, text="Generate", command=create, bg="#2563eb",
              fg="white", activebackground="#1d4ed8", relief="flat",
              padx=22, pady=9).pack(side="left", padx=5)
    tk.Button(buttons, text="Copy", command=copy, bg="#374151",
              fg="white", activebackground="#4b5563", relief="flat",
              padx=22, pady=9).pack(side="left", padx=5)
    root.mainloop()


if __name__ == "__main__":
    main()

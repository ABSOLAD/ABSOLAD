"""Generate a random password using Python's secure secrets module."""

import secrets
import string


def generate_password(length: int, use_upper: bool, use_lower: bool,
                      use_digits: bool, use_symbols: bool) -> str:
    alphabet = ""
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.?/"

    if not alphabet:
        raise ValueError("Select at least one character type.")
    if length < 8:
        raise ValueError("Use a length of at least 8 characters.")

    return "".join(secrets.choice(alphabet) for _ in range(length))


def ask_yes_no(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() == "y"


def main() -> None:
    print("\n=== Password Generator ===")
    try:
        length = int(input("Password length (8 or more): "))
        password = generate_password(
            length,
            ask_yes_no("Include uppercase letters?"),
            ask_yes_no("Include lowercase letters?"),
            ask_yes_no("Include numbers?"),
            ask_yes_no("Include symbols?"),
        )
        print("\nGenerated password:")
        print(password)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

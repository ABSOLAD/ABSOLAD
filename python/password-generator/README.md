# Password Generator

A desktop password generator built with Python and Tkinter. It uses the standard-library `secrets` module rather than ordinary pseudo-random choices.

## Features

- Desktop interface with selectable character groups.
- Password lengths from 8 to 128 characters.
- Guarantees at least one character from each selected group.
- Copy-to-clipboard button.
- No third-party dependencies.

## Run

```bash
python main.py
```

Python 3.8+ with Tkinter is required. On some Linux distributions, Tkinter is installed separately (for example, the `python3-tk` package).

## Tests

```bash
python -m unittest discover -s tests -v
```

## Security note

This is a learning utility, not a password manager. Avoid sharing generated passwords or saving them in source code or screenshots.

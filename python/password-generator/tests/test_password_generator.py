import unittest

from main import generate_password


class PasswordGeneratorTests(unittest.TestCase):
    def test_requested_length(self):
        self.assertEqual(len(generate_password(24, True, True, True, True)), 24)

    def test_selected_groups_are_represented(self):
        password = generate_password(12, True, False, True, False)
        self.assertTrue(any(char.isupper() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertFalse(any(char.islower() for char in password))

    def test_rejects_short_password(self):
        with self.assertRaises(ValueError):
            generate_password(7, True, True, True, True)

    def test_rejects_empty_character_selection(self):
        with self.assertRaises(ValueError):
            generate_password(12, False, False, False, False)


if __name__ == "__main__":
    unittest.main()

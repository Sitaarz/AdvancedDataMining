import unittest

from src.preprocessing.preprocess_data import clean_text, tokenize_text


class TestTextCleaning(unittest.TestCase):

    def test_clean_text_removes_digits_and_punctuation(self):
        text = "Hello World! 12345, how's it going?"
        result = clean_text(text)
        self.assertEqual(result, "helloworldhowsitgoing")

    def test_clean_text_removes_html(self):
        text = "<p>Python is <b>great</b>!</p>"
        result = clean_text(text)
        self.assertEqual(result, "pythonisgreat")

    def test_clean_text_is_lowercase(self):
        text = "ABCDEF"
        result = clean_text(text)
        self.assertEqual(result, "abcdef")

    def test_tokenize_text_splits_words(self):
        text = "Hello, world! It's 2024."
        result = tokenize_text(text)
        self.assertEqual(result, ["helloworldits"])

    def test_clean_text_empty_string(self):
        text = ""
        result = clean_text(text)
        self.assertEqual(result, "")

    def test_tokenize_text_empty_string(self):
        text = ""
        result = tokenize_text(text)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
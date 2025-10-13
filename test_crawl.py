import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        expected = "blog.boot.dev/path"

        test_cases = [
        "https://blog.boot.dev/path/",
        "https://blog.boot.dev/path",
        "http://blog.boot.dev/path/",
        "http://blog.boot.dev/path",
        ]

        for input_url in test_cases:
            with self.subTest(input_url=input_url):
                self.assertEqual(normalize_url(input_url), expected)

if __name__ == "__main__":
    unittest.main()

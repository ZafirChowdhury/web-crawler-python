import unittest

from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html


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

    def test_get_h1_from_html(self):
        # key: value = test_input: expected_output
        input_output_map = {
            "<h1>Hello, from boot.dev</h1>": "Hello, from boot.dev",
            "<h2>This is 2nd heading</h2>": "",
            "<title>Title</title><h1>To be read h1</h1>": "To be read h1",
            "<h1></h1>": "",
            "<h1<h1>": "",  # malformed
            '<h1 class="big">Spicy</h1>': "Spicy",
            " \n <h1>\n spaced \n</h1> ": "spaced",
            "<h1>first</h1><h1>second</h1>": "first",
        }

        for test_case, expected_output in input_output_map.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(get_h1_from_html(test_case), expected_output)

    def test_get_first_paragraph_from_html(self):
        pass
        
        
if __name__ == "__main__":
    unittest.main()

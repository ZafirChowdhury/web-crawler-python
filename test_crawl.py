import unittest

from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_output_map = {
            "https://blog.boot.dev/path/": "blog.boot.dev/path",
            "https://blog.boot.dev/path": "blog.boot.dev/path",
            "http://blog.boot.dev/path/": "blog.boot.dev/path",
            "http://blog.boot.dev/path": "blog.boot.dev/path",

        }

        for test_case, expected_output in input_output_map.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(normalize_url(test_case), expected_output)


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
            "<html><body><h1>Test Title</h1></body></html>": "Test Title",
        }

        for test_case, expected_output in input_output_map.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(get_h1_from_html(test_case), expected_output)


    def test_get_first_paragraph_from_html(self):
        input_output_map = {
            '''<html><body>
                <p>Outside paragraph.</p>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body></html>''' : "Main paragraph.",

            '''<html><body>
                <p>Outside paragraph.</p>
                <main>
                </main>
            </body></html>''' : "Outside paragraph."
        }

        for test_case, expected_output in input_output_map.items():
            with self.subTest(test_case=test_case):
                self.assertEqual(get_first_paragraph_from_html(test_case), expected_output)

           
if __name__ == "__main__":
    unittest.main()

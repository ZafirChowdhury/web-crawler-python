import unittest

from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_output_map = {
            "https://blog.boot.dev/path/": "blog.boot.dev/path",
            "https://blog.boot.dev/path": "blog.boot.dev/path",
            "http://blog.boot.dev/path/": "blog.boot.dev/path",
            "http://blog.boot.dev/path": "blog.boot.dev/path",

        }

        for test_case, expected_output in input_output_map.items():
            print("Running Subtest")
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
            print("Running Subtest")
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
            </body></html>''' : "Outside paragraph.",

            "<html><main> <i>Not p</i> </main></html>": "",

            "<p></P>": "",
        }

        for test_case, expected_output in input_output_map.items():
            print("Running Subtest")
            with self.subTest(test_case=test_case):
                self.assertEqual(get_first_paragraph_from_html(test_case), expected_output)

    
    def test_get_urls_from_html_absolute(self):
        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
        
        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"> <a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev", "https://blog.boot.dev"]
        self.assertEqual(actual, expected)

        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = ''
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

        print("Running Subtest")
        input_url = "www.facebook.com"
        input_body = '<a href="www.facebook.com/zafirChowdhury">'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["www.facebook.com/zafirChowdhury"]
        self.assertEqual(actual, expected)

    
    def test_get_images_from_html_relative(self):
        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body> <img src="/outerImg.png"></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png", "https://blog.boot.dev/outerImg.png"]
        self.assertEqual(actual, expected)

    
    def test_extract_page_data_basic(self):
        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

        print("Running Subtest")
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <main> 
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            </main>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

           
if __name__ == "__main__":
    unittest.main()

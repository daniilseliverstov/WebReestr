import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Edge()

    def tearDown(self):
        self.browser.quit()

    def test_can_start(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("Congratulation", self.browser.title)


if __name__ == "__main__":
    unittest.main()

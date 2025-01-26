import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Edge()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_login_form(self):
        self.browser.get("http://localhost:8000/login/")
        self.assertIn("WebReestr", self.browser.title)

        login_form = self.browser.find_element(By.TAG_NAME, "form")
        self.assertIsNotNone(login_form)
        self.assertIsNotNone(self.browser.find_element(By.NAME, 'username'))
        self.assertIsNotNone(self.browser.find_element(By.NAME, 'password'))
        self.assertIsNotNone(self.browser.find_element(By.TAG_NAME, 'button'))


if __name__ == "__main__":
    unittest.main()

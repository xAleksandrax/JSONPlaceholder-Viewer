import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestJsonPlaceholderViewer(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://xaleksandraxx.pythonanywhere.com/")

    def test_title(self):
        self.assertEqual("", self.driver.title)

    def test_login(self):
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.clear()
        username_input.send_keys('testuser')

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.clear()
        password_input.send_keys('testpass')

        self.driver.find_element(By.CSS_SELECTOR, '.btn1').click()

        welcome_message = self.driver.find_element(By.CSS_SELECTOR, 'h1')
        self.assertEqual(welcome_message.text, 'Welcome back')

    def test_register(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Załóż konto').click()

        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password1').send_keys('testpass')
        self.driver.find_element(By.NAME, 'password2').send_keys('testpass')
        self.driver.find_element(By.CSS_SELECTOR, 'input[value="Zakładam konto"]').click()

        welcome_message = self.driver.find_element(By.CSS_SELECTOR, 'h1')
        self.assertEqual(welcome_message.text, '')


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

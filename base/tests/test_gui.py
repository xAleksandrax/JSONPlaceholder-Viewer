import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class TestJsonPlaceholderViewer(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://xaleksandraxx.pythonanywhere.com/")

    def test_title(self):
        self.assertEqual("", self.driver.title)

    def test_register(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Załóż konto').click()

        self.driver.find_element(By.NAME, 'username').send_keys('testuser2')
        self.driver.find_element(By.NAME, 'password1').send_keys('testpass123')
        self.driver.find_element(By.NAME, 'password2').send_keys('testpass123')
        self.driver.find_element(By.CSS_SELECTOR, 'input[value="Zakładam konto"]').click()

        welcome_message = self.driver.find_element(By.CSS_SELECTOR, 'h1')
        self.assertEqual(welcome_message.text, 'Welcome')

        time.sleep(4)
        
        header = self.driver.find_element(By.CSS_SELECTOR, '.header')
        self.assertIn('Welcome back', header.text)

        self.assertIn('', self.driver.current_url)

    def test_login(self):
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.clear()
        username_input.send_keys('testuser')

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.clear()
        password_input.send_keys('testpass123')

        self.driver.find_element(By.CSS_SELECTOR, '.btn1').click()
        
        time.sleep(4)
        
        header = self.driver.find_element(By.CSS_SELECTOR, '.header')
        self.assertIn('Welcome back', header.text)

        self.assertIn('', self.driver.current_url)

    def test_logout(self):
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.clear()
        username_input.send_keys('testuser')

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.clear()
        password_input.send_keys('testpass123')

        self.driver.find_element(By.CSS_SELECTOR, '.btn1').click()
        
        time.sleep(4)

        self.driver.find_element(By.CSS_SELECTOR, "a[href*='logout']").click()
        time.sleep(2)

        welcome_message = self.driver.find_element(By.CSS_SELECTOR, 'h1')
        self.assertEqual(welcome_message.text, 'Welcome back')

    def test_comments(self):
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.clear()
        username_input.send_keys('testuser')

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.clear()
        password_input.send_keys('testpass123')

        self.driver.find_element(By.CSS_SELECTOR, '.btn1').click()

        self.driver.find_element(By.XPATH, "//button[@class='show-comments']").click()

        time.sleep(2)

        comment_section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment-section')))
        self.assertTrue(comment_section.is_displayed())

        self.driver.find_element(By.XPATH, "//button[@class='show-comments']").click()

        time.sleep(2)

        comment_section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment-section')))
        self.assertFalse(comment_section.is_displayed())

    def test_menu(self):
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.clear()
        username_input.send_keys('testuser')

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.clear()
        password_input.send_keys('testpass123')

        self.driver.find_element(By.CSS_SELECTOR, '.btn1').click()

        albums_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/albums')]")
        filter_link = self.driver.find_element(By.XPATH, "//a[@class='filter-icon']")
        delete_filter_link = self.driver.find_element(By.XPATH, "//a[@class='reset-filters']")

        self.assertTrue(albums_link.is_displayed())
        self.assertTrue(filter_link.is_displayed())

        filter_link.click()
        time.sleep(3)
        filter_options = self.driver.find_elements(By.XPATH, "//ul[@class='filter-posts']//li")

        self.assertTrue(filter_options[0].is_displayed())
        self.assertTrue(filter_options[1].is_displayed())
        self.assertTrue(filter_options[2].is_displayed())

        filter_options[0].click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@class='show-comments']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@class='show-comments']").click()
        delete_filter_link.click()
        time.sleep(2)

        filter_link.click()
        time.sleep(3)
        filter_options = self.driver.find_elements(By.XPATH, "//ul[@class='filter-posts']//li")

        self.assertTrue(filter_options[0].is_displayed())
        self.assertTrue(filter_options[1].is_displayed())
        self.assertTrue(filter_options[2].is_displayed())

        filter_options[1].click()
        time.sleep(2)

        filter_link.click()
        time.sleep(3)
        filter_options = self.driver.find_elements(By.XPATH, "//ul[@class='filter-posts']//li")

        self.assertTrue(filter_options[0].is_displayed())
        self.assertTrue(filter_options[1].is_displayed())
        self.assertTrue(filter_options[2].is_displayed())

        filter_options[2].click()
        time.sleep(2)

        albums_link.click()
        header = self.driver.find_element(By.CSS_SELECTOR, '.header')
        self.assertIn('Welcome back', header.text)  

        self.driver.find_element(By.XPATH, "//button[@class='load-more-button']").click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, "//button[@class='album-button']").click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, "//button[@class='album-button']").click()
        time.sleep(2)

        element = self.driver.find_element(By.CLASS_NAME, 'material-symbols-outlined')
        element.click()


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginNavigationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/")  # Adjust the URL accordingly
        logging.basicConfig(level=logging.INFO)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Fill out the login form
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("me@metu.edu.tr")
        password_input.send_keys("1234")    
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()    
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        logging.info("Logged in successfully")

    def test_dashboard_navigation(self):
        # Fill out the login form
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("me@metu.edu.tr")
        password_input.send_keys("1234")    
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()    
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        # Expand the navbar
        navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        navbar_toggler.click()
        # Wait for the dashboard link to be present
        dashboard_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='dashboard-link']"))
        )
        # Wait for the dashboard link to be clickable
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='dashboard-link']"))
        )
        # Click on the dashboard link in the navbar
        dashboard_link.click()  
        # Wait for the dashboard page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/dashboard"))
        # Check if the user is redirected to the dashboard page
        self.assertIn("/dashboard", self.driver.current_url)
        logging.info("Redirected to dashboard. Current URL: %s", self.driver.current_url)

if __name__ == "__main__":
    unittest.main()

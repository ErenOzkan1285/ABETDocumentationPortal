import unittest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class LoginNavigationTest(unittest.TestCase):

    

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3')  # Suppress logging
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://127.0.0.1:5000/")  # Adjust the URL accordingly
        logging.basicConfig(level=logging.INFO)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Fill out the login form
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("me@metu.edu.tr")
        time.sleep(3)
        password_input.send_keys("1234")    
        time.sleep(3)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(3)
        login_button.click()    
        time.sleep(3)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        logging.info("Logged in successfully")

    def test_dashboard_navigation(self):
        # Fill out the login form
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("me@metu.edu.tr")
        time.sleep(3)
        password_input.send_keys("1234")    
        time.sleep(3)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(3)
        login_button.click()    
        time.sleep(3)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        time.sleep(3)
        # Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(3)
        #navbar_toggler.click()
        time.sleep(3)
        # Wait for the dashboard link to be present
        dashboard_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='dashboard-link']"))
        )
        time.sleep(3)
        # Wait for the dashboard link to be clickable
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='dashboard-link']"))
        )
        time.sleep(3)
        # Click on the dashboard link in the navbar
        dashboard_link.click()  
        time.sleep(3)
        # Wait for the dashboard page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/dashboard"))
        time.sleep(3)
        # Check if the user is redirected to the dashboard page
        self.assertIn("/dashboard", self.driver.current_url)
        logging.info("Redirected to dashboard. Current URL: %s", self.driver.current_url)
        
    def test_coordinator_panel_navigation(self):
    # Fill out the login form with coordinator credentials
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("ee@metu.edu.tr")
        time.sleep(3)
        password_input.send_keys("1234")    
        time.sleep(3)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(3)
        login_button.click()    
        time.sleep(3)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        time.sleep(3)
        ## Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(3)
        #navbar_toggler.click()
        #time.sleep(3)
         #Click on the Coordinator Panel link in the navbar
        coordinator_panel_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='coordinator_panel-link']"))
        )
        time.sleep(3)
        coordinator_panel_link.click()  
        time.sleep(3)
        # Wait for the coordinator panel page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/coordinator_panel"))
        time.sleep(3)
        # Check if the user is redirected to the coordinator panel page
        self.assertIn("/coordinator_panel", self.driver.current_url)
        logging.info("Redirected to Coordinator Panel. Current URL: %s", self.driver.current_url)
        
    def test_admin_panel_navigation(self):
    # Fill out the login form with coordinator credentials
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")  
        email_input.send_keys("yy@metu.edu.tr")
        time.sleep(3)
        password_input.send_keys("1234")    
        time.sleep(3)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(3)
        login_button.click()    
        time.sleep(3)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))   
        time.sleep(3)
        # Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(3)
        #navbar_toggler.click()
        #time.sleep(3)
         #Click on the Admin Panel link in the navbar
        coordinator_panel_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='admin_panel-link']"))
        )
        time.sleep(3)
        coordinator_panel_link.click()  
        time.sleep(3)
        # Wait for the admin panel page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/admin_panel"))
        time.sleep(3)
        # Check if the user is redirected to the admin panel page
        self.assertIn("/admin_panel", self.driver.current_url)
        logging.info("Redirected to Admin Panel. Current URL: %s", self.driver.current_url)



if __name__ == "__main__":
    unittest.main()

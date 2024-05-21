import unittest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

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
        time.sleep(2)
        password_input.send_keys("1234")
        time.sleep(2)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(2)
        login_button.click()
        time.sleep(2)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))
        logging.info("Logged in successfully")

    def test_dashboard_navigation(self):
        # Fill out the login form
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys("me@metu.edu.tr")
        time.sleep(2)
        password_input.send_keys("1234")
        time.sleep(2)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(2)
        login_button.click()
        time.sleep(2)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))
        time.sleep(2)
        # Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(2)
        #navbar_toggler.click()
        time.sleep(2)
        # Wait for the dashboard link to be present
        dashboard_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='dashboard-link']"))
        )
        time.sleep(2)
        # Wait for the dashboard link to be clickable
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='dashboard-link']"))
        )
        time.sleep(2)
        # Click on the dashboard link in the navbar
        dashboard_link.click()
        time.sleep(2)
        # Wait for the dashboard page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/dashboard"))
        time.sleep(2)
        # Check if the user is redirected to the dashboard page
        self.assertIn("/dashboard", self.driver.current_url)
        logging.info("Redirected to dashboard. Current URL: %s", self.driver.current_url)

    def test_coordinator_panel_navigation(self):
        # Fill out the login form with coordinator credentials
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys("ee@metu.edu.tr")
        time.sleep(2)
        password_input.send_keys("1234")
        time.sleep(2)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(2)
        login_button.click()
        time.sleep(2)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))
        time.sleep(2)
        ## Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(2)
        #navbar_toggler.click()
        #time.sleep(2)
        # Click on the Coordinator Panel link in the navbar
        coordinator_panel_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='coordinator_panel-link']"))
        )
        time.sleep(2)
        coordinator_panel_link.click()
        time.sleep(2)
        # Wait for the coordinator panel page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/coordinator_panel"))
        time.sleep(2)
        # Check if the user is redirected to the coordinator panel page
        self.assertIn("/coordinator_panel", self.driver.current_url)
        logging.info("Redirected to Coordinator Panel. Current URL: %s", self.driver.current_url)

    def test_admin_panel_navigation(self):
        # Fill out the login form with admin credentials
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys("yy@metu.edu.tr")
        time.sleep(2)
        password_input.send_keys("1234")
        time.sleep(2)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(2)
        login_button.click()
        time.sleep(2)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))
        time.sleep(2)
        # Expand the navbar
        #navbar_toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        #time.sleep(2)
        #navbar_toggler.click()
        #time.sleep(2)
        # Click on the Admin Panel link in the navbar
        admin_panel_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='admin_panel-link']"))
        )
        time.sleep(2)
        admin_panel_link.click()
        time.sleep(2)
        # Wait for the admin panel page to load
        WebDriverWait(self.driver, 5).until(EC.url_contains("/admin_panel"))
        time.sleep(2)
        # Check if the user is redirected to the admin panel page
        self.assertIn("/admin_panel", self.driver.current_url)
        logging.info("Redirected to Admin Panel. Current URL: %s", self.driver.current_url)
    def test_create_course_instance(self):
        # Fill out the login form with coordinator credentials
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys("ee@metu.edu.tr")
        time.sleep(2)
        password_input.send_keys("1234")
        time.sleep(2)
        # Submit the form
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(2)
        login_button.click()
        time.sleep(2)
        # Wait for the course page to load after successful login
        WebDriverWait(self.driver, 5).until(EC.url_contains("/course"))
        time.sleep(2)
        # Navigate to the Coordinator Panel
        coordinator_panel_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='coordinator_panel-link']"))
        )
        time.sleep(2)
        coordinator_panel_link.click()
        time.sleep(2)
        WebDriverWait(self.driver, 5).until(EC.url_contains("/coordinator_panel"))
        time.sleep(2)
        # Fill out the new course instance form
        course_code_select = Select(self.driver.find_element(By.ID, "course_code"))
        year_input = self.driver.find_element(By.NAME, "year")
        semester_select = Select(self.driver.find_element(By.ID, "semester"))

        course_code_select.select_by_visible_text("140")  # Replace with appropriate value
        time.sleep(2)
        year_input.send_keys("2024")
        time.sleep(2)
        semester_select.select_by_visible_text("Spring")
        time.sleep(2)
        # Submit the form to create the new course instance
        add_course_instance_button = self.driver.find_element(By.XPATH, "//button[@id='add_course_instance_button']")
        time.sleep(2)
        add_course_instance_button.click()
        time.sleep(2)
        # Wait for some indication that the course instance was created
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.assertEqual(alert_text, "Course instance added successfully")
            alert.accept()  # Close the alert
            logging.info("Course instance created successfully with alert: %s", alert_text)
        except NoAlertPresentException:
            self.fail("No alert present after adding course instance")

if __name__ == "__main__":
    unittest.main()

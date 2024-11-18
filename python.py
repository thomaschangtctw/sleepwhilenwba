import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

with open("reservations.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

username = config["login"]["username"]
password = config["login"]["password"]
reservations = config["reservations"]

service = Service("./chromedriver")  # Assumes chromedriver is in the same directory as this script
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://northwestbadmintonacademy.sites.zenplanner.com/login.cfm")
    time.sleep(3)  # Wait for the page to load

    # username and password & login
    username_field = driver.find_element(By.ID, "idUsername")
    password_field = driver.find_element(By.ID, "idPassword")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)  
    time.sleep(5) 

    # Loop through each reservation slot
    for reservation in reservations:
        day = reservation["day"]
        time_slot = reservation["time"]
        person = reservation["person"]

        # Step A: Click on the Calendar link
        calendar_link = driver.find_element(By.LINK_TEXT, "Calendar")
        calendar_link.click()
        time.sleep(3)  # Wait for the page to load

        # Step B: Click on the "Week" button
        week_button = driver.find_element(By.LINK_TEXT, "Week")
        week_button.click()
        time.sleep(3)  # Wait for the week's schedule to load

        # Step C: Find the time slot using the day and time
        time_slot_xpath = f"//div[contains(text(), '{day}: Court Reservation - Slot {time_slot}')]"
        reserve_slot = driver.find_element(By.XPATH, time_slot_xpath)
        reserve_slot.click()
        time.sleep(3)

        # Step D: Select the person from the dropdown
        dropdown = driver.find_element(By.ID, "familyMembers")
        select = Select(dropdown)
        select.select_by_visible_text(person)  # Select the person from the dropdown

        #Step E: Click the "Reserve" button (active reservation)
        reserve_button = driver.find_element(By.ID, "reserve_1")
        reserve_button.click()  # Click the "Reserve" button
        time.sleep(3)

finally:
    driver.quit()

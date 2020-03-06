# autoAdd method using selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary

usernameStr = "shuo_wang" # enter your ucsbNetID
passwordStr = "20130532@Wws" # enter your password (PS: PLZ do not upload your code with your password. I don't want to know that lol)

def autoAdd(s1):
    browser = webdriver.Chrome()
    browser.get(("https://my.sa.ucsb.edu/gold/Login.aspx"))

    username = browser.find_element_by_id("pageContent_userNameText")
    username.send_keys(usernameStr)
    password = browser.find_element_by_id("pageContent_passwordText")
    password.send_keys(passwordStr)

    # sign_in
    signInButton = browser.find_element_by_id("pageContent_loginButton")
    signInButton.click()

    # continue
    continueButton = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, "pageContent_continueButton")))
    continueButton.click()

    # change quarter
    quarterSelect = Select(browser.find_element_by_id("ctl00_pageContent_quarterDropDown"))
    quarterSelect.select_by_value('20202')

    # enter enrollcode
    enrollCode = browser.find_element_by_id("ctl00_pageContent_EnrollCodeTextBox")
    enrollCode.send_keys(s1)
    addButton = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, "ctl00_pageContent_AddCourseButton")))
    addButton.click()

    # add to schedule
    addScheduleButton = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, "pageContent_AddToScheduleButton")))
    addScheduleButton.click()




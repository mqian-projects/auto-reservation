from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from otu_gen import get_code
from otu_gen import get_user_pw
import time
import os


def run(res_time, res_type, seed=0):
    # hour = int(datetime.now().strftime("%H"))

    # if hour >= 0 and hour <= 5:
    #     print("Program does not function between midnight and 6:00AM.")
    #     return

    otu_code = get_code(seed)
    username_password = get_user_pw()
    username_signin = username_password[0]
    password_signin = username_password[1]
    UID_signin = username_password[2]

    option = Options()
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    # intiate browser
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    wait = WebDriverWait(browser, 15)

    # open website and click through
    browser.get(
        'https://www.imleagues.com/spa/account/ssoredirect?schoolId=4395e0c781af4905a4088a9561509399')
    wait.until(EC.element_to_be_clickable((By.ID, "ssoDirect"))).click()

    # filling in login info
    username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username.send_keys(username_signin)
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password.send_keys(password_signin)

    wait.until(EC.element_to_be_clickable(
        (By.NAME, "_eventId_proceed"))).click()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Please complete your multi-factor authentication using Duo.')]")))
    browser.switch_to.frame("duo_iframe")

    # need to identify the cancel button etc
    cancel = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "btn-cancel")))
    cancel.click()

    # enter a passcode
    passcode_btn = wait.until(EC.element_to_be_clickable((By.ID, "passcode")))
    passcode_btn.click()

    passcode = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "passcode-input")))
    # generating and receiving passcodes needs to be automated, doing manually for now
    passcode.send_keys(otu_code)

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "passcode")))
    submit_btn.click()

    reserve = wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Reservations")))
    reserve.click()

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//body/div[@id='mainView']/div[1]/div[11]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/week-calendar[1]/div[2]/div[2]")))

    next_day = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[11]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/week-calendar[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/button[2]")))
    next_day.click()

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//body/div[@id='mainView']/div[1]/div[11]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/week-calendar[1]/div[2]/div[2]")))

    eppley_spot = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(), '" + res_type + "')]/following-sibling::div[contains(text(), '" + res_time + "')]/../following-sibling::div/div[1]/button[1]")))

    eppley_spot.click()

    password = wait.until(EC.presence_of_element_located((By.NAME, "txtSID")))
    password.send_keys(UID_signin)

    reserve_final = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Sign Up')]")))
    reserve_final.click()

    time.sleep(10)
    browser.quit()
    return


# def lambda_handler(event, context):
#     print("This is the event {}".format(event))
#     # this format must be used exactly
#     # time: 10:00 AM
#     time_workout = "10:00 AM"
#     type_workout = "Individual Workout: Weight Room (ERC)"
#     run(time_workout, type_workout)

time_workout = "10:00 AM"
type_workout = "Individual Workout: Weight Room (ERC)"
run(time_workout, type_workout)

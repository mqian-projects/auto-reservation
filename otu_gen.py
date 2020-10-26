import csv
import os.path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def get_code(seed_code):
    if os.path.isfile('./otu_codes.csv'):
        code_and_numrows = get_code_numrows()

        if code_and_numrows[1] < 19:
            return code_and_numrows[0]
        else:
            # last code, clearing csv, adding new codes
            file_fill(code_and_numrows[0])
            new_code_and_numrows = get_code_numrows()
            return new_code_and_numrows[0]
    else:
        # if file is not yet there
        file = open("otu_codes.csv", "x")
        file.close()
        # hardcode a known code here to get started
        file_fill(seed_code)
        new_code_and_numrows = get_code_numrows()
        return new_code_and_numrows[0]


def file_fill(code):
    # clears file and replaces with new codes
    file1 = open("otu_codes.csv", 'w')
    writer = csv.writer(file1, lineterminator='\n')
    # hardcode a known code here to get started
    new_codes = retrieve_codes(code)
    writer.writerows(new_codes)
    file1.close()
    return


def get_code_numrows():
    file_r = open('./otu_codes.csv', 'r')
    reader = csv.reader(file_r, dialect='excel')
    num_rows = sum(1 for row in reader)
    file_r.seek(0)
    code = ''
    for i in range(0, num_rows - 9):
        code = next(reader)
    file_r.close()
    file_w = open("otu_codes.csv", 'a')
    writer = csv.writer(file_w, lineterminator='\n')
    writer.writerow("FILL")
    file_w.close()
    return [code, num_rows]


def get_user_pw():
    filename = "C:\\Users\\micha\\Desktop\\misc\\login.csv"
    file_r = open(filename, 'r')
    reader = csv.reader(file_r)
    username = next(reader)
    password = next(reader)
    UID = next(reader)
    file_r.close()
    return [username, password, UID]


def retrieve_codes(last_key):
    iter_codes = []
    username_password = get_user_pw()
    username_signin = username_password[0]
    password_signin = username_password[1]

    # intiate browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(browser, 15)

    browser.get('https://identity.umd.edu/mfaprofile')

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
    passcode.send_keys(last_key)

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "passcode")))
    submit_btn.click()

    gen_codes_btn = wait.until(
        EC.element_to_be_clickable((By.NAME, "printBypassCodes")))
    gen_codes_btn.click()

    browser.switch_to.alert.accept()

    # wait.until(EC.element_located_to_be_selected((By.CLASS_NAME, "SubDisplayElementFlex")))
    time.sleep(5)
    codes = browser.find_elements_by_class_name("SubDisplayElementFlex")

    for i in range(0, 10):
        iter_codes.insert(i, [codes[i].text])

    return iter_codes

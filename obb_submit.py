import os
import time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

url = "https://www.openbugbounty.org/report/"
#url = "https://gmail.com"
bugs = open("obb.txt", "r").readlines()
secound = [7,6,5]

options = Options()
#options.binary_location = "/usr/bin/google-chrome"
options.add_argument("user-data-dir=/tmp/chrome")

driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

def submit(bug):
    time.sleep(random.choice(secound))
    driver.find_element_by_class_name('checkmark').click()
    select = Select(driver.find_element_by_name('type'))
    select.select_by_visible_text("Cross Site Scripting (XSS)")
    link = driver.find_element_by_name("url")
    link.clear()
    link.send_keys(bug)
    driver.find_element_by_class_name('checkmarkr').click()
    time.sleep(random.choice(secound))
    try:
        captcha = driver.find_element_by_class_name("g-recaptcha")
        print("Captcha Found\nSolve it And Press Enter")
        os.system("spd-say 'manul checkpoin please check, manul checkpoin please check'")
        raw_input()
        time.sleep(random.choice(secound))
    except NoSuchElementException:
        print("No captcha")
    driver.find_element_by_name("report").click()

for bug in bugs:
    print(bug.strip())
    submit(bug.strip())
    print("Done\n")

driver.quit()

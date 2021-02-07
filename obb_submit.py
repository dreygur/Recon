#!/usr/bin/env python3

"""
Coded: Rakibul Yeasin (@dreygur)
For: Tanzil Hasan Khan (the_choura_guy)
"""

import os
import sys
import time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Timeout
from time import sleep
from random import randint

# Detect Platform
if "win" in sys.platform:
	driver = "driver.exe"
elif "linux" in sys.platform:
	driver = "driver"

# Service
path = os.path.join(os.getcwd(), 'driver/chrome' + driver)
print(path)
service = Service(path)

# Options
options = Options()
options.add_argument("user-data-dir=./driver/chromecache")

# Driver Object
try:
	driver = webdriver.Chrome(options=options, service=service)
except:
	driver = webdriver.Chrome(options=options, executable_path=path)

creds = {
	"user": "",
	"pass": ""
}


def login():
	urls = [
		'https://mail.google.com',
		'https://google.com',
		'https://duckduckgo.com',
		'https://github.com',
		'https://mobile.facebook.com'
	]

	for uri in urls:
		print(f"[Debug] Visiting: {uri}")
		driver.get(uri)
		sleep(randint(3, 10))

	driver.get('https://www.openbugbounty.org/report/')
	sleep(3)

	try:
		twitter = driver.find_element_by_xpath("//input[@type='image']")
		twitter.click()
		sleep(3)
		user_inp = driver.find_element_by_id("username_or_email")
		user_inp.send_keys(creds.get("user"))
		pass_inp = driver.find_element_by_id("password")
		pass_inp.send_keys(creds.get("pass"))
		submit = driver.find_element_by_id("allow")
		sleep(3)
		submit.send_keys(Keys.RETURN)
	except NoSuchElementException:
		print("[Debug] Already LOGGED in!")
	sleep(10)

def submit(bug):
    url = "https://www.openbugbounty.org/report/"
    secound = [10,8,8]
    driver.get(url)

    time.sleep(random.choice(secound))
    eth = driver.find_element_by_id("agreeethics")
    eth.click()
    # driver.find_element_by_class_name('checkmark').click()
    select = Select(driver.find_element_by_name('type'))
    select.select_by_visible_text("Cross Site Scripting (XSS)")
    link = driver.find_element_by_name("url")
    link.clear()
    link.send_keys(bug)
    # confirm = driver.find_element_by_id("confirm_auto")
    # confirm.click()
    driver.find_element_by_class_name('checkmarkr').click()
    time.sleep(random.choice(secound))

    try:
        driver.find_element_by_class_name("g-recaptcha")
        print("Captcha Found\nSolve it And Press Enter")
        os.system("spd-say 'manul checkpoin please check, manul checkpoin please check'")
        raw_input()
        time.sleep(random.choice(secound))
    except NoSuchElementException:
        print("No captcha")
    driver.find_element_by_name("report").click()

def main():
	bugs = open("obb.txt", "r").readlines()

	login()

	for bug in bugs:
	    print(bug.strip())
	    submit(bug.strip())
	    print("Done\n")

if __name__ == '__main__':
	main()
	driver.quit()

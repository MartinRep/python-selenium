#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Command to hide browser window when executing
import os
os.environ['MOZ_HEADLESS'] = '1'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities =
		{
			'waitForReady': True,
			'applicationType': 'Device'
        },
    options=chrome_options)

try:
    browser.get('http://192.168.1.254')
    password_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'login_password')))
    password_input.click()
    password_input.send_keys('# ROUTER PASSWORD #' + Keys.RETURN)
    down_usage = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'home_total_down_flow')))
    whole_text = down_usage.text
    print("Download usage in details:{} {}".format(whole_text[:-2], whole_text[-2:]))
    logout_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@onclick='EMUI.LogoutObjController.Logout();']")))
    logout_button.click()
    browser.quit()
except Exception as e:
    print(e)


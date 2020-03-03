from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os
os.environ['MOZ_HEADLESS'] = '1'

browser = webdriver.Firefox(executable_path='./geckodriver')

browser.get('http://192.168.1.254')

password_input = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, 'login_password')))
password_input.click()
password_input.send_keys('PASSWORD' + Keys.RETURN)

down_usage = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, 'home_total_down_flow')))
whole_text = down_usage.text
print(f'Download usage: {whole_text} In details: {whole_text[:-2]} {whole_text[-2:]}')

logout = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@onclick='EMUI.LogoutObjController.Logout();']"))).click()

browser.quit()

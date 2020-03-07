#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import mysql.connector as mariadb

# Command to hide browser window when executing
import os
os.environ['MOZ_HEADLESS'] = '1'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Remote(
    command_executor='http://192.168.1.1:4444/wd/hub',
    options=chrome_options)

try:
    browser.get('http://192.168.1.254')
    password_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'login_password')))
    password_input.click()
    password_input.send_keys('##PASSWORD##' + Keys.RETURN)
    down_usage = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'home_total_down_flow')))
    whole_text = down_usage.text
    print("Download usage in details:{} {}".format(whole_text[:-2], whole_text[-2:]))
    logout_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@onclick='EMUI.LogoutObjController.Logout();']")))
    logout_button.click()
    browser.quit()
except Exception as e:
    print(e)

mariadb_connection = mariadb.connect(user='worker', database='mysql', host='192.168.1.1')
cursor = mariadb_connection.cursor(buffered=True)
cursor.execute("SHOW TABLES LIKE 'dl_usage'")
if(cursor.rowcount < 1):
    cursor.execute("CREATE TABLE dl_usage( measurement_id INT(11) NOT NULL AUTO_INCREMENT,  timestamp TIMESTAMP,  value FLOAT(5,1), unit VARCHAR(2), CONSTRAINT measurement_pk PRIMARY KEY (measurement_id))")
# else:
#     cursor.execute("DROP TABLE dl_usage")

sql = "INSERT INTO dl_usage (value, unit) VALUES (%s, %s)"
val = [float(whole_text[:-2]), str(whole_text[-2:])]
cursor.execute(sql, val)
mariadb_connection.commit()
cursor.close()


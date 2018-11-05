from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random

# 模拟输入
def _input_simulation(e, text):
    for i in range(len(text)):
        sleep_time = random.randint(8, 30)
        time.sleep(sleep_time / 10)
        e.send_keys(text[i])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
#os.environ["webdriver.chrome.driver"] = 'C:\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome('C:\\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
url = "https://pub.alimama.com/"
browser.get(url)

locator = (By.ID, 'mx_n_18')
WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
target = browser.find_element_by_xpath('//div[@id="mx_n_18"]/ul/li[2]')

print("target:", target)
target.click()

time.sleep(3)
with open("a.txt","w",encoding='utf-8') as f:
    f.write(browser.page_source)

login_iframe= browser.find_element_by_name('alimamaLoginIfr')
browser.switch_to.frame(login_iframe)

locator = (By.ID, 'J_logname')
WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
username = browser.find_element_by_id('J_logname')
print("J_logname:", username)
time.sleep(3)
username.clear()
_input_simulation(username, '敖乐的小号1')

password = browser.find_element_by_id('J_logpassword')
print("J_logpassword:", password)
password.clear()
_input_simulation(password,'Ml1637019')

time.sleep(30)
#submit = browser.find_element_by_xpath('//*[@id="fm1"]/input[9]')
submit = browser.find_element_by_id("J_submit")
print("submit:", submit)
submit.click()



time.sleep(600)
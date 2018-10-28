
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
print("xiaojie")
url = "https://passport.csdn.net/account/login"
try:
    browser.get(url)
    #print(browser.page_source)
    #target = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/h3/a')
    target = browser.find_element_by_css_selector("div.login-part>h3>a")
    print("target:", target)
    target.click()

    locator = (By.ID, 'username')
    WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
    username = browser.find_element_by_id('username')
    print("username:", username)
    time.sleep(3)
    username.clear()
    username.send_keys('1544915738@qq.com')

    password = browser.find_element_by_id('password')
    print("password:", password)
    password.clear()
    password.send_keys('@#Mlcsdn7019')

    #submit = browser.find_element_by_xpath('//*[@id="fm1"]/input[9]')
    submit = browser.find_element_by_css_selector("form#fm1>input.logging")
    print("submit:", submit)
    submit.click()

    url="https://download.csdn.net/download/concn117/10251164"
    browser.get(url)
    direct_download = browser.find_element_by_xpath('//*[@class="direct_download"]')
    direct_download.click()
    time.sleep(3)
        #down_er = browser.find_element_by_xpath('//div[@id="noVipNoEnoughPHasC]/div[@class="dl_download_btn"]/a')
    try:
        down_er = browser.find_element_by_css_selector('div#noVipNoEnoughPHasC>div.dl_download_btn>a[data-href^="https"]')
    except Exception:
        try:
            down_er = browser.find_element_by_css_selector('div#download>div.dl_download_btn>a[data-href^="https"]')
        except Exception:
            raise Exception("downer is null")

    time.sleep(3)
    #print(browser.page_source)
    down_er.click()
except Exception as e:
    print(e)
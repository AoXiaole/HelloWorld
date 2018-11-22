
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

def 浏览器初始化():
    global browser
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')


def 获取流通股东排名_腾讯(证券名):
    text = []

    url = "http://gu.qq.com/{0}/gp".format(证券名)
    try:
        browser.get(url)
        locator = (By.XPATH, '//div[@class="mod-detail write mod-ltgd"]/div[2]/table[2]/tbody')
        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))

        target = browser.find_element_by_xpath('//div[@class="mod-detail write mod-ltgd"]/div[2]/table[2]/tbody')

        trlist = target.find_elements_by_tag_name("tr")

        for i in range(len(trlist)):
            doc = pq(trlist[i].get_attribute('innerHTML'))
            items = doc('td')
            text.append(items.text())
    except Exception as e:
        print(e)

    return text


tt=获取流通股东排名_腾讯('sh600436')
print('tt:',tt)
exit(0)
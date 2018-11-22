# _*_encoding:UTF-8_*_
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,time,random
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

#browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
browser = None

def 浏览器初始化():
    global browser
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

#证券名 不带前缀
# 返回值
def 同花顺_获取流通股东排名(证券名):
    text = []
    time_list = []
    changed_text = []
    data_list = []
    data_node_list = []
    value = {}
    try:
        try:
            url = "http://stockpage.10jqka.com.cn/{0}/holder/".format(证券名)
            browser.get(url)
            print("url:",url)
        except Exception as e:
            time.sleep(2)
            browser.get(url)
            print(e)
        try:
            locator = (By.ID, 'dataifm')
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
            # switch_to.frame 默认是使用id和name来定位的
            browser.switch_to.frame('dataifm')
            locator = (By.ID, 'bd_1')
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
            target = browser.find_element_by_id('bd_1')
        except Exception as e:
            print(e)
            # 有些证券没有流通股
            return

            # target.get_attribute('innerHTML') 获取html 文本
        doc = pq(target.get_attribute('innerHTML'))

        # 根据属性名来选择
        time_list_pq = doc('a[targ="fher_1"]').parent().parent().children('li')
        # 获取时间列表
        for it in time_list_pq.items():
            time_list.append(it.text())

        十大流通股东排名列表_times_pq =  doc('.m_tab_content2.clearfix')

        # 获取 十大流通股 变化信息
        for it in 十大流通股东排名列表_times_pq.items():
            changed_pq = it.find("table").find("caption")
            data_pq = changed_pq.parent().find("tbody").find("tr")
            data_node_list= []
            for it_it in data_pq.items():
                text = it_it.text().replace('点击查看', '').split('\n')
                data_node_list.append(text)
            data_list.append(data_node_list)

            changed_text.append(changed_pq.text())

        for i in range(len(time_list)):
           value[time_list[i]] = dict({'info':changed_text[i]})
           value[time_list[i]] = dict({"status":data_list[i]})
    except Exception as e:
        print(e)
        # 有些证券没有流通股
        return

    return value

def 同花顺_更新沪深A最新股票列表():
    value = []
    browser.get('http://q.10jqka.com.cn/')
    locator = (By.CLASS_NAME, 'page_info')
    WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
    target = browser.find_element_by_class_name('page_info')
    # target.text 获取selenium 文本
    pages = target.text.split('/')[1]

    for i in range(1, int(pages) + 1):
        time.sleep(random.uniform(1, 2))
        locator = (By.CSS_SELECTOR, '#m-page>a[page="{0}"]'.format(i))
        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
        next_page = browser.find_element_by_css_selector('#m-page>a[page="{0}"]'.format(i))

        next_page.click()
        locator = (By.ID, 'maincont')
        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
        target = browser.find_element_by_css_selector('#maincont>table>tbody')
        doc = pq(target.get_attribute('innerHTML'))
        lists = doc('tr')
        for node in lists.items():
            value.append([x for x in node.text().split('\n')])

    with open('mm/stock_list.py','w+',encoding='utf-8') as f:
        f.write("stock_list_day_data={0}".format(value))

    return value

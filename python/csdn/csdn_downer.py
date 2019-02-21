#!/usr/bin/python3
from selenium import webdriver
import os,re,sys
import socket
import json
import time,threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from mymodule.csdn_config import *

g_task_running = 0
g_quit = 0

down_base_dir = G_CSDN.down_dir
chrome_driver_file = G_CSDN.chromedriver_dir
log_dir = G_CSDN.log_dir
log_file = ''  # 在init中会初始化

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0, 'download.default_directory': down_base_dir})
browser = webdriver.Chrome(chrome_driver_file, chrome_options=chrome_options)
browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

def selenium_find_element(locator):

    WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
    return browser.find_element(locator[0], locator[1])

def thread_sleep(s):
    while not g_quit and s > 0 :
        time.sleep(1)
        s = s-1

#创建日志文件
def log_int(url):
    global log_file
    log_file = log_dir + re.sub(re.compile(r'\W', re.S), "", url)

def log(msg):
    global log_file
    print(msg)
    try:
        with open(log_file,'a+') as f:
            f.write(msg)
            f.write('\n')
    except Exception as err:
        print('write log failed',err)
        return 0
    return 1

def scdn_login():
    log('login ...')
    browser.get("https://passport.csdn.net/login")
    target = selenium_find_element((By.LINK_TEXT,"帐号登录"))
    target.click()
    log('input username and passwd')
    username = selenium_find_element((By.ID,'all'))
    time.sleep(1)
    username.clear()
    username.send_keys('1544915738@qq.com')

    password = selenium_find_element((By.ID,'password-number'))

    password.clear()
    password.send_keys('@#Mlcsdn7019')

    submit = browser.find_element_by_css_selector("button.btn.btn-primary")
    submit.click()
    log('login success.')

def get_down_er():
    down_er = selenium_find_element((By.ID, 'noVipEnoughP'))
    if down_er.is_displayed():
        return down_er.find_element(By.CSS_SELECTOR, "div.resource_dl_btn>a")

    #if down_er.find_element_by_css_selector('a[href^="javascript:"]').get_attribute('class') == 'pop_close':


    down_er = selenium_find_element((By.ID, 'download'))
    if down_er.is_displayed():
        return down_er.find_element(By.CSS_SELECTOR, "div.dl_download_btn>a")


    return None


def download(url):

    browser.get(url)
    down_dir = down_base_dir + re.sub(re.compile(r'\W',re.S),"",url)

    if not os.path.exists(down_dir):
        os.makedirs(down_dir)

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': down_dir}}
    browser.execute("send_command", params)
    log('created download dir :' + down_dir)

    direct_download = selenium_find_element((By.CLASS_NAME, 'direct_download'))

    thread_sleep(5)
    direct_download.click()
    log('click direct_download')

    down_er = get_down_er()
    if not down_er:
        raise Exception('get_down_er failed')

    log('get down_er')
    down_er.click()
    log('downloading...')

    check_down_is_ok(down_dir)

    return down_dir

def check_down_is_ok(dir):

        timeout=20
        while not os.listdir(dir) and timeout:
            log('not found file')
            thread_sleep(1)
            timeout = timeout -1

        if timeout == 0:
            log('timeout')
            raise Exception('down load timeout')

        file = os.listdir(dir)[0]
        while '.crdownload' == file[-11:]:
            thread_sleep(2)
            file = os.listdir(dir)[0]

        log("file name:" + dir + file)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("failed! param : [url]")
        exit(-1)
    url = sys.argv[1]
    print(url)
    try:
        log_int(url)
        scdn_login()
        thread_sleep(1)
        down_dir = download(url)
    except Exception as err:
        print('failed',err)
        exit(-1)
    if not down_dir:
        print("download failed")

    print('download success dir:',down_dir)
    exit(0)

#!/usr/bin/python3
from selenium import webdriver
import os,re,sys

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def remov_dir(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            remov_dir(file_path)
        else:
            os.remove(file_path)

    os.rmdir(path)

def thread_sleep(s):
    while  s > 0 :
        time.sleep(1)
        s = s-1

class CSDN:
    browser = None
    downing = False
    logined = False
    down_base_dir = 'E:\work\download\\'
    log_dir = 'E:\work\download\log\\'
    chromedriver_dir = 'C:\\Users\Dell\AppData\Local\Google\Chrome\Application\chromedriver.exe'

    def __init__(self):
        pass


    def chrome_open(self):
        if CSDN.browser:
            return
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0,
                                                         'download.default_directory': CSDN.down_base_dir})
        CSDN.browser = webdriver.Chrome(CSDN.chromedriver_dir, chrome_options=chrome_options)
        CSDN.browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    def selenium_find_element(self, locator):
        WebDriverWait(CSDN.browser, 20, 0.5).until(EC.presence_of_element_located(locator))
        return CSDN.browser.find_element(locator[0], locator[1])

    def log(self, msg):
        print(msg)
        try:
            with open(self.log_file, 'a+') as f:
                f.write(msg)
                f.write('\n')
        except Exception as err:
            print('write log failed', err)
            return 0
        return 1

    def scdn_login(self):
        if CSDN.logined:
            return
        self.log('login ...')
        CSDN.browser.get("https://passport.csdn.net/login")
        target = self.selenium_find_element((By.LINK_TEXT, "帐号登录"))
        target.click()
        self.log('input username and passwd')
        username = self.selenium_find_element((By.ID, 'all'))
        time.sleep(1)
        username.clear()
        username.send_keys('1544915738@qq.com')

        password = self.selenium_find_element((By.ID, 'password-number'))

        password.clear()
        password.send_keys('ao1021111230')

        submit = CSDN.browser.find_element_by_css_selector("button.btn.btn-primary")
        submit.click()
        self.log('login success.')
        CSDN.logined = True

    def _downer_handle(self):
        downer = self.selenium_find_element((By.ID, 'noVipEnoughP'))
        if downer.is_displayed():
            return downer.find_element(By.CSS_SELECTOR, "div.resource_dl_btn>a")

        downer = self.selenium_find_element((By.ID, 'download'))
        if downer.is_displayed():
            return downer.find_element(By.CSS_SELECTOR, "div.dl_download_btn>a")

        return None

    def _get_file(self, dir):

        timeout=20
        while not os.listdir(dir) and timeout:
            self.log('not found file')
            thread_sleep(1)
            timeout = timeout -1

        if timeout == 0:
            self.log('timeout')
            raise Exception('down load timeout')

        file = os.listdir(dir)[0]
        while '.crdownload' == file[-11:]:
            thread_sleep(2)
            file = os.listdir(dir)[0]

        self.log("file name:" + os.path.join(dir, file))
        return os.path.join(dir, file)

    def _download(self):

        CSDN.browser.get(self.url)

        if not os.path.exists(self.down_dir):
            os.makedirs(self.down_dir)

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.down_dir}}
        CSDN.browser.execute("send_command", params)
        self.log('created download dir :' + self.down_dir)

        direct_download = self.selenium_find_element((By.CLASS_NAME, 'direct_download'))

        thread_sleep(5)
        direct_download.click()
        self.log('click direct_download')

        downer = self._downer_handle()
        if not downer:
            raise Exception('_downer_handle failed')

        self.log('get down_er')
        downer.click()
        self.log('downloading...')

        filename = self._get_file(self.down_dir)

        return filename


    def csdn_download(self,url):

        # 若文件已经存在，则返回文件名
        temp = re.sub(re.compile(r'\W', re.S), "", url)
        temp_dir = os.path.join(CSDN.down_base_dir, temp)
        if os.path.exists(temp_dir):
            filename = os.listdir(temp_dir)[0]
            if filename:
                return os.path.join(temp_dir, filename)

        # 等待之前的任务是否完成
        timeout = 20
        while CSDN.downing and timeout > 0:
            thread_sleep(1)
            timeout = timeout - 1
        if CSDN.downing:
            return None

        CSDN.downing = True
        self.url = url
        self.log_file = os.path.join(CSDN.log_dir, temp)
        self.down_dir = os.path.join(CSDN.down_base_dir, temp)

        try:
            self.chrome_open()

            self.scdn_login()
            thread_sleep(1)
            file = self._download()
            if not file:
                raise Exception('download failed')
            print('download success :', file)
            CSDN.downing = False
            return file

        except Exception as err:
            print('failed',err)

            if os.path.exists(self.down_dir):
                remov_dir(self.down_dir)

            CSDN.downing = False
            return None


# def chrome_open():
#     global  browser
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--no-sandbox")
#     #chrome_options.add_argument("--headless")
#     chrome_options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0, 'download.default_directory': down_base_dir})
#     browser = webdriver.Chrome(chrome_driver_file, chrome_options=chrome_options)
#     browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
#
# def selenium_find_element(locator):
#
#     WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
#     return browser.find_element(locator[0], locator[1])
#

#
# #创建日志文件
# def log_init(url):
#     log_file = log_dir + re.sub(re.compile(r'\W', re.S), "", url)
#     def l_write(msg):
#         print(msg)
#         try:
#             with open(log_file,'a+') as f:
#                 f.write(msg)
#                 f.write('\n')
#         except Exception as err:
#             print('write log failed',err)
#             return 0
#         return 1
#     return l_write
#
# def scdn_login():
#     log('login ...')
#     browser.get("https://passport.csdn.net/login")
#     target = selenium_find_element((By.LINK_TEXT,"帐号登录"))
#     target.click()
#     log('input username and passwd')
#     username = selenium_find_element((By.ID,'all'))
#     time.sleep(1)
#     username.clear()
#     username.send_keys('1544915738@qq.com')
#
#     password = selenium_find_element((By.ID,'password-number'))
#
#     password.clear()
#     password.send_keys('@#Mlcsdn7019')
#
#     submit = browser.find_element_by_css_selector("button.btn.btn-primary")
#     submit.click()
#     log('login success.')
#
# def _downer_handle():
#     down_er = selenium_find_element((By.ID, 'noVipEnoughP'))
#     if down_er.is_displayed():
#         return down_er.find_element(By.CSS_SELECTOR, "div.resource_dl_btn>a")
#
#     #if down_er.find_element_by_css_selector('a[href^="javascript:"]').get_attribute('class') == 'pop_close':
#
#
#     down_er = selenium_find_element((By.ID, 'download'))
#     if down_er.is_displayed():
#         return down_er.find_element(By.CSS_SELECTOR, "div.dl_download_btn>a")
#
#     return None
#
#
# def download(url):
#
#     browser.get(url)
#     down_dir = down_base_dir + re.sub(re.compile(r'\W',re.S),"",url)
#
#     if not os.path.exists(down_dir):
#         os.makedirs(down_dir)
#
#     params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': down_dir}}
#     browser.execute("send_command", params)
#     log('created download dir :' + down_dir)
#
#     direct_download = selenium_find_element((By.CLASS_NAME, 'direct_download'))
#
#     thread_sleep(5)
#     direct_download.click()
#     log('click direct_download')
#
#     down_er = _downer_handle()
#     if not down_er:
#         raise Exception('_downer_handle failed')
#
#     log('get down_er')
#     down_er.click()
#     log('downloading...')
#
#     filename = check_down_is_ok(down_dir)
#
#     return filename
#
# def check_down_is_ok(dir):
#
#         timeout=20
#         while not os.listdir(dir) and timeout:
#             log('not found file')
#             thread_sleep(1)
#             timeout = timeout -1
#
#         if timeout == 0:
#             log('timeout')
#             raise Exception('down load timeout')
#
#         file = os.listdir(dir)[0]
#         while '.crdownload' == file[-11:]:
#             thread_sleep(2)
#             file = os.listdir(dir)[0]
#
#         log("file name:" + os.path.join(dir, file))
#         return os.path.join(dir, file)
#

#
# def csdn_download(url):
#     global  log
#     down_dir = down_base_dir + re.sub(re.compile(r'\W',re.S),"",url)
#     if os.path.exists(down_dir):
#         filename = os.listdir(down_dir)[0]
#         if filename:
#             return os.path.join(down_dir, filename)
#
#     try:
#         chrome_open()
#         log = log_init(url)
#         scdn_login()
#         thread_sleep(1)
#         file = download(url)
#         if not file:
#             raise Exception('download failed')
#         print('download success :', file)
#         browser.quit()
#         return file
#
#     except Exception as err:
#         print('failed',err)
#         if browser:
#             browser.quit()
#
#         if os.path.exists(down_dir):
#             remov_dir(down_dir)
#
#         return None
#
#
#
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("failed! param : [url]")
        exit(-1)
    uurl = sys.argv[1]
    print(uurl)
    csdner = CSDN()
    file = csdner.csdn_download(uurl)

    print("file:",file)

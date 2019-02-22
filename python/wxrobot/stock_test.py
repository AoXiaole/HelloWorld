from stock.tenxun.tenxun import *
from stock.tonghuashun.ths import *
import os,time
if __name__ == '__main__':

    code_list = 腾讯_获取A股股票代码(8000)
    for code in code_list:
        if not os.path.exists(company_brief_dir + "/{0}.txt".format(code[-6:])):
            time.sleep(0.2)
            print("更新:",code)
            同花顺_更新公司简介(code[-6:])

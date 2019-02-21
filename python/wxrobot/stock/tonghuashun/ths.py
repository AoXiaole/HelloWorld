# encoding:utf-8
import requests,json
from pyquery import PyQuery as pq
import xlrd
import os
def DEBUG(str):
    pass
log = DEBUG
def 同花顺_获取公司单季度财务数据(code):
    data_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }
    #获取xls表格
    p_get = requests.get('http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=simple&code={0}'.format(code), headers=headers)

    workbook = xlrd.open_workbook(file_contents = p_get.content)

    sheet1 = workbook.sheet_by_index(0)

    for i in range(sheet1.ncols):
        coldata = sheet1.col_values(i)
        data_list.append(coldata[1:])

    for i in range(len(data_list)):
        log(data_list[i])

def 同花顺_更新公司详细信息(code):
    ata_list = []

    if os.path.isfile('stock_data/company_detail/company_detail_{0}'.format(code)):
        return False
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }
    # 获取xls表格
    p_get = requests.get('http://basic.10jqka.com.cn/{0}/company.html'.format(code),
                         headers=headers)

    # 解决中文乱码的问题
    # https://www.cnblogs.com/Yemilice/p/6201224.html
    #<meta http-equiv="Content-Type" content="text/html; charset=gbk"/>
    p_get.encoding = 'GBK'
    #print(p_get.text)
    doc = pq(p_get.text)
    data = doc("#publish").text()
    log(data)
    if data :
        with open('stock_data/company_detail/company_detail_{0}'.format(code),'w') as f:
            f.write(data)
        return True
    else:
        return False

if __name__ == '__main__':
    log = print
    同花顺_更新公司详细信息('300209')
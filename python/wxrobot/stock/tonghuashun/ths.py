# encoding:utf-8
import requests,json
from pyquery import PyQuery as pq
import xlrd
import os
def DEBUG(str):
    pass
log = DEBUG

finance_dir = "./data/stock/finance"
company_brief_dir = './data/stock/brief'

def 同花顺_更新公司单季度财务数据(code):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }
    # 获取xls表格
    p_get = requests.get(
        'http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=simple&code={0}'.format(code),
        headers=headers)

    with open(finance_dir + '/' + code + '.xlsx',"wb+") as f:
        f.write(p_get.content)


def 同花顺_获取公司单季度财务数据(code):
    '''
    按行读取[
    ['科目\\时间', '2018-09-30', ]
    ['基本每股收益', -0.0981, -0.0006,]
    ['净利润(元)', -28525100.000000004, -181500.0, ]
    ['净利润同比增长率', '-153.48%', '-101.34%', '23.54%',]
    ...
    ]

    '''
    data_list = []
    workbook = xlrd.open_workbook(finance_dir + '/' + code + '.xlsx')

    sheet1 = workbook.sheet_by_index(0)

    for i in range(1,sheet1.nrows):
        rowdata = sheet1.row_values(i)
        data_list.append(rowdata)

    for i in range(len(data_list)):
        log(data_list[i])

    return data_list

def 同花顺_更新公司简介(code):

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
        with open(company_brief_dir + '/{0}.txt'.format(code),'w+') as f:
            f.write(data)
        return True
    else:
        return False

if __name__ == '__main__':
    finance_dir = "./test_data"
    company_brief_dir = './test_brief'
    log = print
    同花顺_获取公司单季度财务数据('300209')
# encoding:utf-8
import requests,json
from pyquery import PyQuery as pq
import xlrd,time
from stock.tenxun.tenxun import *
from  stock.tenxun.code_name import *

from requests.cookies import RequestsCookieJar
import os
#http://d.10jqka.com.cn/v2/realhead/hs_000006/last.js  获取000006 基本数据

def DEBUG(str):
    pass
log = DEBUG

finance_dir = "./data/stock/finance"
company_brief_dir = './data/stock/brief'
comment_dir = './data/stock/点评'

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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }

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

#点评项 = ['代码','名称','评分','点评']
点评项 = ['代码', '名称', '评分', '机构数','持股','流通股占比','点评']
def 同花顺_获取点评(code):
    '''
    #code 不带 前缀
    '''
    data_list = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }
    # 获取xls表格
    p_get = requests.get('http://stockpage.10jqka.com.cn/{0}/'.format(code), headers=headers)
    if p_get.status_code != 200:
        return None
    doc = pq(p_get.text)
    data = doc(".fl.analyze-result.clearfix").text()
    if not data:
        return None
    data_list['代码'] = code
    head = 'sh' if code[0] == '6' else 'sz'

    data_list['名称'] = 腾讯_代码名称[head + code]

    data_list['评分']= data.split(' ')[0]
    if data_list['评分'] == '--':
        data_list['评分'] = '-1'

    data_list['点评'] = data

    机构数 = ''
    持股 = ''
    流通股占比 = ''

    t = re.search(r'迄今为止，共(.*)主力机构', data, re.S)
    if t:
        机构数 = t.group(1)
    t = re.search(r'持仓量总计(.*)股，占流通A股(.*)近期的平均成本', data, re.S)
    if t:
        持股 = t.group(1)
        流通股占比 = t.group(2)
    data_list['机构数'] = 机构数
    data_list['持股'] = 持股
    data_list['流通股占比'] = 流通股占比


    log(data_list)

    return data_list

def 同花顺_更新点评文件():
    big_data_array = []

    code_list = 腾讯_代码名称.keys()

    ok_code = []
    time_max = 200
    haveBreak = True  # 给个初始值
    # 循环获取，直到所有数据都拿下
    while haveBreak and time_max > 0:
        time_max = time_max -1
        haveBreak = False
        for code in code_list:
            if code in ok_code:
                continue
            time.sleep(0.1)
            temp = 同花顺_获取点评(code[2:])
            if temp:
                big_data_array.append(temp)
                ok_code.append(code)
                log('获取成功:{0}'.format(code))
            else:
                haveBreak = True
                log('获取失败:{0}'.format(code))


    writebook = xlwt.Workbook()
    sheet = writebook.add_sheet('test')


    nums = len(点评项)
    for i in range(nums):
        sheet.write(0, i, 点评项[i])

    line = 1
    for code_data in big_data_array:
        for i in range(nums):
            sheet.write(line, i, code_data.get(点评项[i], ''))
        line = line + 1

    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    filename = os.path.join(comment_dir, "{0}.xlsx".format(day))
    # 文件存在，将文件删除
    if os.path.isfile(filename):
        os.remove(filename)

    writebook.save(filename)



def test():
    列表名 =  ['代码', '名称', '评分', '机构数','持股','流通股占比','点评']
    data_list = []

    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    workbook = xlrd.open_workbook(os.path.join(comment_dir, "{0}.xlsx".format(day)))
    writebook = xlwt.Workbook()
    wsheet = writebook.add_sheet('test')

    sheet1 = workbook.sheet_by_index(0)

    for i in range(1, sheet1.nrows):

        temp_map = {}
        data = sheet1.row_values(i)
        temp_map['代码'] = data[0]
        temp_map['名称'] = data[1]
        temp_map['评分'] = data[2]
        temp_map['点评'] = data[3]
        机构数 = ''
        持股= ''
        流通股占比 = ''

        t = re.search(r'迄今为止，共(.*)主力机构', data[3], re.S)
        if t:
            机构数 = t.group(1)
        t = re.search(r'持仓量总计(.*)股，占流通A股(.*)近期的平均成本', data[3], re.S)
        if t:
            持股 = t.group(1)
            流通股占比 = t.group(2)
        temp_map['机构数'] = 机构数
        temp_map['持股'] = 持股
        temp_map['流通股占比'] = 流通股占比

        data_list.append(temp_map)


    line = 1
    nums = len(列表名)
    for i in range(nums):
        wsheet.write(0, i, 列表名[i])

    for code_data in data_list:
        for i in range(nums):
            wsheet.write(line, i, code_data.get(列表名[i], ''))
        line = line + 1

    new_book = os.path.join(comment_dir, "{0}_new.xlsx".format(day))
    # 文件存在，将文件删除
    if os.path.isfile(new_book):
        os.remove(new_book)

    writebook.save(new_book)
if __name__ == '__main__':
    finance_dir = "./test_data"
    company_brief_dir = './test_brief'
    comment_dir = './test_data/点评'
    log = print
    #test()

    同花顺_获取点评('000001')
    # 同花顺_更新股票基本数据('000002')
    # 同花顺_更新股票基本数据('000004')
    # 同花顺_更新股票基本数据('000005')
    # 同花顺_更新股票基本数据('000006')
    # 同花顺_更新股票基本数据('000007')
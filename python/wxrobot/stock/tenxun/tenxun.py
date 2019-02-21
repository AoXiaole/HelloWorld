# encoding:utf-8
import requests,json
from pyquery import PyQuery as pq
import re

# 时间轴
# http://stock.gtimg.cn/data/index.php?appn=detail&action=timeline&c=sh600532
#
# 第几页的实时数据
# http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sh600532&p=25
#
# 当前实时数据，10挡行情
# http://web.sqt.gtimg.cn/q=sh600532
#
#
# 日线数据，日K数据是按年获取的
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sz002468,day,2011-01-01,2011-12-31,320,qfq
#
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh600315,day,2004-01-01,2004-12-31,320,qfq
#
# 经过测试发现也可以不按年获取
#
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh600315,day,2000-01-01,2004-12-31,320,qfq
#
# 高斯贝尔日K图
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sz002848,day,2000-01-01,2019-12-31,320,qfq
#
#
# 周K
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param=sz002848,week,2017-01-01,2017-12-31,320,qfq
#
#
# 月K
# http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_monthqfq&param=sz002848,month,,,320


def DEBUG(str):
    pass
log = DEBUG

def 腾讯_实时数据分段列表(code):

    p_get=requests.get('http://stock.gtimg.cn/data/index.php?appn=detail&action=timeline&c={0}'.format(code))
    time_list = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('|')
    log(time_list)
    return time_list

#腾讯实时数据是分段获取的，时间段的获取在函数 ‘腾讯_实时数据分段列表’；num 下标从 0 开始
#返回数据格式为[[0,],[1]]
def 腾讯_第N段实时数据(code, num):
    data_list = []
    p_get = requests.get('http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c={0}&p={1}'.format(code, num))
    string = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('|')
    #print(data_list)
    for i in range(len(string)):
        data_list.append(tuple(string[i].split('/')))
    return data_list

def 腾讯_获取当天实时数据(code):
    day_data=[]
    time_list = 腾讯_实时数据分段列表(code)
    num = len(time_list)
    log(num)
    for i in range(num):
        day_data += 腾讯_第N段实时数据(code, i)
    log(day_data)
    return day_data

def 腾讯_获取当前实时数据(code):
    p_get = requests.get('http://web.sqt.gtimg.cn/q={0}'.format(code))
    string = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('~')
    log(string)
    return string

# 返回上海证券交易所开市时间列表，[年-月-日,]
def 腾讯_获取上证历史日时间表(year):
    p_get = requests.get('http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh000001,day,{0}-01-01,{0}-12-31,320,qfq'.format(year))
    #执行表达式语句
    exec(p_get.text)

    #计算表达式的值
    var = eval(p_get.text.split("=")[0])
    day_list = var['data']['sh000001']['day']
    data_list  = [d[0] for d in day_list]
    log(data_list)
    return data_list

def 腾讯_获取上证历史周时间表(year):
    p_get = requests.get(
        'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param=sh000001,week,{0}-01-01,{0}-12-31,320,qfq'.format(
            year))
    # 执行表达式语句
    exec(p_get.text)

    # 计算表达式的值
    var = eval(p_get.text.split("=")[0])
    week_list = var['data']['sh000001']['week']
    week_list = [d[0] for d in week_list]
    log(week_list)
    return week_list

#获取某只股票某年的日数据，日数据包括[时间，开盘价，收盘价，最高价，最低价，成交量(手)]
def 腾讯_获取一年的日线数据(year, code):
    return 腾讯_获取日线数据("{0}-01-01".format(year),"{0}-12-31".format(year),code)

#时间格式是 1990-01-01,日数据包括[时间，开盘价，收盘价，最高价，最低价，成交量(手)]
def 腾讯_获取日线数据(day_start,day_end,code):
    p_get = requests.get(
        'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={0},day,{1},{2},320,qfq'.format(
            code, day_start, day_end))
    # 执行表达式语句
    exec(p_get.text)
    # 计算表达式的值
    var = eval(p_get.text.split("=")[0])
    day_list = var['data'][code]['qfqday']
    log(day_list)
    return day_list

#获取某只股票某年的周数据，周数据包括[时间，开盘价，收盘价，最高价，最低价，成交量(手)]
def 腾讯_获取一年的周线数据(year, code):
    return 腾讯_获取周线数据("{0}-01-01".format(year),"{0}-12-31".format(year),code)

#时间格式是 1990-01-01,周数据包括[时间，开盘价，收盘价，最高价，最低价，成交量(手)]
def 腾讯_获取周线数据(week_start,week_end,code):
    p_get = requests.get(
        'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param={0},week,{1},{2},320,qfq'.format(
            code, week_start, week_end))
    # 执行表达式语句
    exec(p_get.text)
    # 计算表达式的值
    var = eval(p_get.text.split("=")[0])
    week_list = var['data'][code]['qfqweek']
    log(week_list)
    return week_list

def 腾讯_获取A股股票代码(maxnum):
    p_get = requests.get('http://stock.gtimg.cn/data/index.php?appn=rank&t=ranka/chr&p=1&o=0&l={0}&v=list_data'.format(maxnum))
    # 执行表达式语句
    log( p_get.text)
    code_list = re.findall(r'data:\'([^\']*)\'', p_get.text, re.S)[0].split(",")
    log(code_list)
    return code_list

if __name__ == '__main__':
    log = print

    # day_list = 腾讯_获取上证历史日时间表(2018)
    # week_list = 腾讯_获取上证历史周时间表(2018)
    #
    # print(day_list)
    # print(week_list)
    #
    # day_data = 腾讯_获取日线数据(day_list[-10], day_list[-1], 'sh600315')
    # week_data = 腾讯_获取周线数据(week_list[-10], week_list[-1], 'sh600315')
    # 当天数据 = 腾讯_获取当天实时数据('sh600315')
    #
    # print(day_data)
    # print(week_data)
    # print(当天数据)

    code_list = 腾讯_获取A股股票代码(8000)
    log("A股一共{0}只股票".format(len(code_list)))
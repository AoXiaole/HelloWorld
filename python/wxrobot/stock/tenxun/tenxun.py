# encoding:utf-8
import requests,json,xlrd,xlwt
from pyquery import PyQuery as pq
import re,pprint,time,os
from stock.tenxun.code_name import *

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

#获取基本实时数据信息
#http://web.sqt.gtimg.cn/q=sz000002
baseinf_day_dir = './data/stock/baseinfo_day'
tenxun_dir = './stock/tenxun'
def DEBUG(str):
    pass
log = DEBUG

def code_prefix(code):
    return 'sh' if code[0] == '6' else 'sz'

def tencent_request_get(request_url):
    p_get=requests.get(request_url)
    if p_get.status_code != 200:
        raise Exception('http respond is {0}'.format(p_get.status_code))

    return p_get

def 腾讯_实时数据时间段列表(code):

    p_get=tencent_request_get('http://stock.gtimg.cn/data/index.php?appn=detail&action=timeline&c={0}'.format(code_prefix(code) + code))
    time_list = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('|')
    log(time_list)
    return time_list

#腾讯实时数据是分段获取的，时间段的获取在函数 ‘腾讯_实时数据时间段列表’；num 下标从 0 开始
#返回数据格式为[[0,],[1]]
def 腾讯_第N段交易数据(code, num):
    data_list = []
    p_get = tencent_request_get('http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c={0}&p={1}'.format(code_prefix(code) + code, num))
    string = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('|')
    #print(data_list)
    for i in range(len(string)):
        data_list.append(tuple(string[i].split('/')))
    return data_list

def 腾讯_获取当天交易数据(code):
    day_data=[]
    time_list = 腾讯_实时数据时间段列表(code)
    num = len(time_list)
    log(num)
    for i in range(num):
        day_data += 腾讯_第N段交易数据(code, i)
    log(day_data)
    return day_data

def 腾讯_获取当前实时数据(code):
    p_get = tencent_request_get('http://web.sqt.gtimg.cn/q={0}'.format(code_prefix(code) + code))

    string = re.findall(r'[^"]*"([^"]*)"', p_get.text, re.S)[0].split('~')
    log(string)
    return string

# 返回上海证券交易所开市时间列表，[年-月-日,]
def 腾讯_获取上证历史日时间表(year):
    p_get = tencent_request_get('http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh000001,day,{0}-01-01,{0}-12-31,320,qfq'.format(year))

    #执行表达式语句
    exec(p_get.text)

    #计算表达式的值
    var = eval(p_get.text.split("=")[0])
    day_list = var['data']['sh000001']['day']
    data_list  = [d[0] for d in day_list]
    log(data_list)
    return data_list

def 腾讯_获取上证历史周时间表(year):
    p_get = tencent_request_get(
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
    p_get = tencent_request_get(
        'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={0},day,{1},{2},320,qfq'.format(
            code_prefix(code) + code, day_start, day_end))
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
    p_get = tencent_request_get(
        'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param={0},week,{1},{2},320,qfq'.format(
            code_prefix(code) + code, week_start, week_end))
    # 执行表达式语句
    exec(p_get.text)
    # 计算表达式的值
    var = eval(p_get.text.split("=")[0])
    week_list = var['data'][code]['qfqweek']
    log(week_list)
    return week_list

# 返回 [000001,...]
def 腾讯_获取A股股票代码(maxnum):
    p_get = requests.get('http://stock.gtimg.cn/data/index.php?appn=rank&t=ranka/chr&p=1&o=0&l={0}&v=list_data'.format(maxnum))
    # 执行表达式语句
    log( p_get.text)
    code_list = re.findall(r'data:\'([^\']*)\'', p_get.text, re.S)[0].split(",")
    log(code_list)
    data_list = [i[2:] for i in code_list]
    return data_list


def 腾讯_获取A股实时数据文件(filepath):
    '''
    获取A股所有股票的实时数据，返回一个execl文件
    :param filepath:
    :return:
    '''
    # 获取xls表格
    p_get = requests.get('http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr')

    with open(filepath, "wb+") as f:
        f.write(p_get.content)

def 腾讯_获取A股实时数据():
    '''
    获取实时数据，返回一个数据字典

    {'code1':{'名称':'','最新价':''...}
     code2':{'名称':'','最新价':''...}
    }
    code 带前缀
    :return:
    '''
    data_list = {}
    name = []
    # 获取xls表格
    p_get = requests.get('http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr')
    if p_get.status_code != 200:
        return None
    workbook = xlrd.open_workbook(file_contents=p_get.content)

    sheet1 = workbook.sheet_by_index(0)
    name = sheet1.row_values(1)

    for i in range(2, sheet1.nrows):
        data = {}
        rowdata = sheet1.row_values(i)
        for n in range(1,len(rowdata)):
            data[name[n]] = rowdata[n]
        data_list[rowdata[0]] = data

    # for k,v in data_list.items():
    #     print(k,":",v)

    return data_list

基本信息名称列表=[(1,'名称'),(2,'代码'),(3,'当前价'),(4,'昨收'),(32,'涨幅'),(31,'涨价'),(43,'振幅'),(5,'今开'),
          (33,'最高'),(34,'最低'),(36,'成交量手'),(37,'成交额万'),(44,'流通市值亿'),(45,'总市值亿'),(38,'换手率'),
          (49,'量比'),(39,'T市盈率'),(53,'H市盈率静'),(52,'H市盈率动'),(46,'市净率'),(47,'涨停'),(48,'跌停')]

def 腾讯_获取个股实时基本数据信息(code):
    '''http://web.sqt.gtimg.cn/q=sz000002
    返回 {'当前价':'','今开',''...}

     成交量 单位为手
     成交额单位为 万
     市值单位为 亿
    '''
    data_list = {}
    try:
        p_get = requests.get('http://web.sqt.gtimg.cn/q={0}'.format(code_prefix(code) + code))
        if p_get.status_code != 200:
            return None
    except Exception :
        return None

    templist = re.search(r'="(.*)"', p_get.text, re.S).group(1).split("~")
    if len(templist) < 54:
        return None
    for item in 基本信息名称列表:
        data_list[item[1]] = templist[item[0]]
    print(data_list)
    return data_list


def 腾讯_获取多股实时基本数据信息(code_list):
    '''
    :param code_list: 不带前缀
    :return: {codei: {'名称':'','':,'':}}
    '''
    big_data_array = {}
    haveBreak = True # 给个初始值
    try_times_max = 5
    # 循环获取，直到所有数据都拿下
    while haveBreak and try_times_max > 0:
        haveBreak = False
        for code in code_list:
            if code in big_data_array.keys():
                continue
            temp = 腾讯_获取个股实时基本数据信息(code)
            if temp :
                big_data_array[code] = temp
                print('获取成功:{0}'.format(code))
            else :
                haveBreak = True
                print('获取失败:{0}'.format(code))
            time.sleep(0.1)
        try_times_max = try_times_max -1
    return big_data_array

def 腾讯_更新股票基本数据文件(filename):
    '''
    将当前的股票的基本信息数据写入execl文件
    文件格式 年-月-日.execl
    :return:
    '''

    # 将上证的数据，全部拿下，在写入文件
    big_data_array = []
    code_list = 腾讯_获取A股股票代码(8000)

    ok_code = []
    haveBreak = True # 给个初始值
    # 循环获取，直到所有数据都拿下
    while haveBreak:
        haveBreak = False
        for code in code_list:
            if code in ok_code:
                continue
            temp = 腾讯_获取个股实时基本数据信息(code)
            if temp :
                big_data_array.append(temp)
                ok_code.append(code)
                log('获取成功:{0}'.format(code))
            else :
                haveBreak = True
                log('获取失败:{0}'.format(code))

    writebook = xlwt.Workbook()
    sheet = writebook.add_sheet('test')
    line = 1
    nums = len(基本信息名称列表)
    for i in range(nums):
        sheet.write(0, i, 基本信息名称列表[i][1])

    for code_data in big_data_array:
        for i in range(nums):
            sheet.write(line, i, code_data.get(基本信息名称列表[i][1],''))
        line = line + 1

    #day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #filename = os.path.join(baseinf_day_dir, "{0}.xlsx".format(day))
    # 文件存在，将文件删除
    if os.path.isfile(filename):
        os.remove(filename)

    writebook.save(filename)

    return True




def 腾讯_获取股票基本数据():
    '''
    获取所有股票当前基本信息，从文件获取
    :return:
    '''


def 腾讯_获取股票名称(code):
    try:
        p_get = requests.get('http://web.sqt.gtimg.cn/q={0}'.format(code_prefix(code) + code))
        if p_get.status_code != 200:
            return None
    except Exception as err:
        return None

    templist = re.search(r'="(.*)"', p_get.text, re.S).group(1).split("~")
    print(p_get.text)
    if len(templist) > 1:
        return templist[1]
    else:
        return None


def 腾讯_获取股票名称_EX(code_list):
    '''
    code_list 是不带前缀的 []
    返回 {codei:namei}
    '''
    code_name = {}

    haveBreak = True  # 给个初始值
    # 循环获取，直到所有数据都拿下
    while haveBreak:
        haveBreak = False
        for code in code_list:
            if code in code_name.keys():
                continue
            name = 腾讯_获取股票名称(code)
            if name:
                code_name[code] = name
                log('获取成功:{0}'.format(code))
            else:
                haveBreak = True
                log('获取失败:{0}'.format(code))
    return code_name


def 腾讯_更新股票列表(total):

    code_name = {}

    code_list = 腾讯_获取A股股票代码(total)
    haveBreak = True  # 给个初始值
    # 循环获取，直到所有数据都拿下
    while haveBreak:
        haveBreak = False
        for code in code_list:
            if code in code_name.keys():
                continue
            name = 腾讯_获取股票名称(code)
            if name:
                code_name[code] = name
                log('获取成功:{0}'.format(code))
            else:
                haveBreak = True
                log('获取失败:{0}'.format(code))

    with open(os.path.join(tenxun_dir,'code_name.py'),'w',encoding='utf-8') as f:
        f.write('# encoding:utf-8\n')
        f.write("腾讯_代码名称={0}".format(json.dumps(code_name)))
    return code_name


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
    baseinf_day_dir = './test_baseinfo_day'
    tenxun_dir = './'
    腾讯_获取当天交易数据('000001')
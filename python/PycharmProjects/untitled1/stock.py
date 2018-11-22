from mm.tonghuashun import *
from mm.stock_list import *
import os,time,random

if __name__ == '__main__':
    data_list = {}
    浏览器初始化()
    # 同花顺_更新沪深A最新股票列表()
    codec_list = {}
    for item in stock_list_day_data:
        codec_list[item[1]] = item[2]

    for key in codec_list.keys():
    #for key in ['603421']:
        time.sleep(random.uniform(0.1, 2))
        value = 同花顺_获取流通股东排名(key)
        print(value)
        data_list[key] = value

    with open('mm/stock_tenlist.py','w+',encoding='utf-8') as f:
        f.write("stock_tenlist_data={0}".format(data_list))

    print(data_list)


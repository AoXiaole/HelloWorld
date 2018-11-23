from mm.tonghuashun import *
from mm.stock_list import *
from mm.stock_tenlist import *

import os,time,random
import pymysql

db_host = '118.25.239.224'
db_user = 'longint'
db_pw = 'longint@LONGINT9136'
db_name = 'stock_db'
g_conn = pymysql.connect(host='118.25.239.224',port= 3306,user = 'longint',passwd='longint@LONGINT9136',db='stock_db')
g_cur = g_conn.cursor()

def write_mysql_ten( tenlist):
    pass

def create_ten_table(codec,time_str):
    tale_name='ten_{0}_{1}'.format(codec,time_str)
    sql_str = "create table  if not exists {0} (".format(tale_name) + \
                  "name varchar(256) not NULL, " +\
                  "nums varchar(20) not NULL, " +\
                  "a_change varchar(40) not NULL, " +\
                  "scale varchar(40) not NULL, " +\
                  "cost varchar(40) not NULL, " +\
                  "active_change varchar(40) not NULL , " +\
                  "primary key(name)" +\
                  ")"
    #sql_str = "create table ten_ee_90 ( name varchar(256) not NULL, primary key(name))"
    print("sql_str:",sql_str)
    g_cur.execute(sql_str)

def get_stock_tenlist():
    data_list = {}
    浏览器初始化()
    # 同花顺_更新沪深A最新股票列表()
    codec_list = {}
    for item in stock_list_day_data:
        codec_list[item[1]] = item[2]

    #for key in codec_list.keys():
    for key in ['603421']:
        time.sleep(random.uniform(0.1, 2))
        value = 同花顺_获取流通股东排名(key)
        print(value)
        for time_, value in value.items():
            create_ten_table(key, time_.replace('-','_'))
            value_list = []
            for li in value.get('status',[]):
                value_list.append(tuple(li[:-1]))

            for li in value_list:
                print(li)
                g_cur.executemany("insert into ten_{0}_{1} values(%s,%s,%s,%s,%s,%s)".format(key,time_.replace('-','_')), [li])
            g_conn.commit()

        #data_list[key] = value

    #with open('mm/stock_tenlist.py','w+',encoding='utf-8') as f:
    #   f.write("stock_tenlist_data={0}".format(data_list))

    #print(data_list)


get_stock_tenlist()
g_cur.close()
g_conn.close()
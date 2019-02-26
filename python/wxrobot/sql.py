#!/usr/bin/python3
# encoding:utf-8

import pymysql,time,xlrd
from stock.tenxun.tenxun import *


def create_table_by_execl(db, execl_file):
    day_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    table_name = 't_' + day_str
    cursor = db.cursor()
    workbook = xlrd.open_workbook(execl_file)

    sheet1 = workbook.sheet_by_index(0)
    name = sheet1.row_values(1)


    # print(name)
    # print(value)

    cursor.execute("DROP TABLE IF EXISTS `{0}`".format(table_name))

    insert_head = 'INSERT INTO `{0}` (`代码`, `名称`, `最新价`, `涨跌幅`, `涨跌额`, `成交量`, `成交额`, `今开`, `昨收`, `最高`, `最低`) VALUES'.format(table_name)
    # 使用预处理语句创建表
    sql = """CREATE TABLE `{0}` ( 
        `代码` CHAR(6) NOT NULL, 
        `名称` VARCHAR(20) NULL, 
        `最新价` FLOAT NULL DEFAULT 0.0, 
        `涨跌幅` FLOAT NULL DEFAULT 0.0, 
        `涨跌额` FLOAT NULL DEFAULT 0.0, 
        `成交量` INT(8) NULL DEFAULT 0, 
        `成交额` FLOAT NULL DEFAULT 0.0, 
        `今开` FLOAT NULL DEFAULT 0.0, 
        `昨收` FLOAT NULL DEFAULT 0.0, 
        `最高` FLOAT NULL DEFAULT 0.0, 
        `最低` FLOAT NULL DEFAULT 0.0, 
        PRIMARY KEY (`代码`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8;""".format(table_name)

    cursor.execute(sql)

    db.commit()

    insert_list = ""
    for i in range(2, sheet1.nrows):
        data = sheet1.row_values(i)
        insert_list += '''('{0}','{1}',{2},{3},{4},{5},{6},{7},{8},{9},{10}),'''.format(
            data[0][2:], data[1], data[2], data[3], data[4], data[7], data[8], data[9], data[10],
            data[11], data[12]
        )

    sql = insert_head + insert_list[:-1]

    cursor.execute(sql)
    db.commit()

def update_code_name_table(db):
    cursor = db.cursor()
    # 获取 最新的代码(不带前缀)列表
    new_code_set = set(腾讯_获取A股股票代码(8000))

    # 获取数据库中已经存在的代码
    sql = '''SELECT code FROM t_code_name;'''
    cursor.execute(sql)
    results = cursor.fetchall()

    sql_code_set = {i[0] for i in results}
    add_code_set = new_code_set - sql_code_set

    # 获取数据库中需要更新的代码
    sql = '''SELECT code FROM t_code_name where need_update = 1;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    update_code_set = {i[0] for i in results}

    code_set = add_code_set | update_code_set

    new_code_name = 腾讯_获取股票名称_EX(code_set)


    insert_head = 'INSERT INTO `t_code_name` (`code`, `name`,`need_update`) VALUES'
    insert_list = ""

    # 插入新的
    for code in add_code_set:

        insert_list += '''('{0}','{1}',{2}),'''.format(
            code, new_code_name[code], 1 if new_code_name[code][0] == 'D' or new_code_name[code][0] == 'S' or new_code_name[code][0] == 'N' else 0
        )

    sql = insert_head + insert_list[:-1]
    cursor.execute(sql)

    #更新需要更新的
    for code in update_code_set:
        if new_code_name[code][0] == 'D' or new_code_name[code][0] == 'S' or new_code_name[code][0] == 'N':
            continue

        sql = '''UPDATE `t_code_name` SET `name`='{0}', `need_update`='0' WHERE `code`='{1}';'''.format(new_code_name[code],code)
        cursor.execute(sql)

    db.commit()



def update_all_code_name_table(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `t_code_name`")

    # 使用预处理语句创建表
    sql = """CREATE TABLE `t_code_name` ( 
            `code` CHAR(6) NOT NULL,
            `name` VARCHAR(20) NOT NULL,
            `need_update` TINYINT NOT NULL DEFAULT 0,
            PRIMARY KEY (`code`))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""

    cursor.execute(sql)

    db.commit()

    insert_head = 'INSERT INTO `t_code_name` (`code`, `name`,`need_update`) VALUES'
    insert_list = ""
    code_list = 腾讯_更新股票列表(8000)

    for k ,v in code_list.items():
        insert_list += '''('{0}','{1}',{2}),'''.format(
            k[2:] , v ,  1 if v[0] == 'D' or v[0] == 'S' or v[0] == 'N' else 0
        )

    sql = insert_head + insert_list[:-1]
    cursor.execute(sql)
    db.commit()

# 打开数据库连接
db = pymysql.connect("localhost", "root", "000000", "dbstock")

#create_table_by_execl(db, '2019-02-25.xls')

#update_all_code_name_table(db)
update_code_name_table(db)
# 关闭数据库连接
db.close()


#!/usr/bin/python3
# encoding:utf-8

import pymysql,time,xlrd


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

# 打开数据库连接
db = pymysql.connect("localhost", "root", "000000", "dbstock")

create_table_by_execl(db, '2019-02-25.xls')


# 关闭数据库连接
db.close()


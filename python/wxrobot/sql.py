#!/usr/bin/python3
# encoding:utf-8
from multiprocessing import Pool
import pymysql,time,xlrd
from stock.tenxun.tenxun import *
from mycommon.common import *


def create_table_by_execl(db, execl_file):
    day_str = time.strftime('%Y_%m_%d', time.localtime(time.time()))
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
    sql = '''SELECT code FROM `dbstock`.`t_code_name` where need_update = 1;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    update_code_set = {i[0] for i in results}

    code_set = add_code_set | update_code_set

    new_code_name = 腾讯_获取股票名称_EX(code_set)


    insert_head = 'INSERT INTO `dbstock`.`t_code_name` (`code`, `name`,`need_update`) VALUES'
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

        sql = '''UPDATE `dbstock`.`t_code_name` SET `name`='{0}', `need_update`='0' WHERE `code`='{1}';'''.format(new_code_name[code],code)
        cursor.execute(sql)

    db.commit()



def update_all_code_name_table(db):

    code_list = 腾讯_获取A股股票代码(8000)
    code_name = 腾讯_获取股票名称_EX(code_list)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `dbstock`.`t_code_name`")

    # 使用预处理语句创建表
    sql = """CREATE TABLE `dbstock`.`t_code_name` ( 
                `code` CHAR(6) NOT NULL,
                `name` VARCHAR(20) NOT NULL,
                `need_update` TINYINT NOT NULL DEFAULT 0,
                PRIMARY KEY (`code`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8;"""

    cursor.execute(sql)

    db.commit()

    insert_head = 'INSERT INTO `dbstock`.`t_code_name` (`code`, `name`,`need_update`) VALUES'
    insert_list = ""
    for k ,v in code_name.items():
        insert_list += '''('{0}','{1}',{2}),'''.format(
            k, v,  1 if v[0] == 'D' or v[0] == 'S' or v[0] == 'N' else 0
        )

    sql = insert_head + insert_list[:-1]
    cursor.execute(sql)
    db.commit()

def get_v(value):
    return value if value and value != '--' else "-999999.99"


def save_AG_day_data(db):
    table_name = 't_ag_day_{0}'.format(time.strftime('%Y_%m_%d', time.localtime(time.time())))
    code_list = 腾讯_获取A股股票代码(8000)
    ag_day_data = 腾讯_获取多股实时基本数据信息(code_list)
    # 测试
    # with open(os.path.join(tenxun_dir,'code_name.py'),'w',encoding='utf-8') as f:
    #     f.write('# encoding:utf-8\n')
    #     f.write("腾讯={0}".format(json.dumps(ag_day_data)))

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `dbstock`.`{0}`".format(table_name))

    # 使用预处理语句创建表
    sql = """CREATE TABLE `dbstock`.`{0}` (
    `代码` CHAR(6) NOT NULL,
    `名称` CHAR(6) NOT NULL,   
    `当前价` FLOAT NOT NULL,
    `涨幅` FLOAT NOT NULL,
    `涨价` FLOAT NOT NULL,
    `昨收` FLOAT NOT NULL,
    `今开` FLOAT NOT NULL,
    `最高` FLOAT NOT NULL,
    `最低` FLOAT NOT NULL,
    `振幅` FLOAT NOT NULL,
    `成交量手` FLOAT NOT NULL COMMENT '单位为手',
    `成交额万` FLOAT NOT NULL COMMENT '单位为万',
    `流通市值亿` FLOAT NOT NULL COMMENT '单位为亿',
    `总市值亿` FLOAT NOT NULL COMMENT '单位为亿',
    `换手率` FLOAT NOT NULL,
    `量比` FLOAT NOT NULL,
    `T市盈率` FLOAT NOT NULL,
    `H市盈率静` FLOAT NOT NULL,
    `H市盈率动` FLOAT NOT NULL,
    `市净率` FLOAT NOT NULL,
    `涨停` FLOAT NOT NULL,
    `跌停` FLOAT NOT NULL,
    PRIMARY KEY (`代码`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8;""".format(table_name)

    cursor.execute(sql)
    db.commit()

    insert_head = 'INSERT INTO `dbstock`.`{0}` (`代码`, `名称`,`当前价`,`涨幅`,`涨价`, \
    `昨收`,`今开`,`最高`,`最低`,`振幅`,`成交量手`,`成交额万`,`流通市值亿`,`总市值亿`,`换手率`, \
    `量比`, `T市盈率`,`H市盈率静`,`H市盈率动`,`市净率`,`涨停`,`跌停`) VALUES'.format(table_name)
    insert_list = ""

    for k ,v in ag_day_data.items():
        insert_list += '''('{0}','{1}',{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21}),'''.format(
            k, get_v(v['名称']), get_v(v['当前价']),get_v(v['涨幅']),get_v(v['涨价']),get_v(v['昨收']),get_v(v['今开']),get_v(v['最高']),get_v(v['最低']),get_v(v['振幅']),
            get_v(v['成交量手']),get_v(v['成交额万']),get_v(v['流通市值亿']),get_v(v['总市值亿']),get_v(v['换手率']),get_v(v['量比']),get_v(v['T市盈率']),
            get_v(v['H市盈率静']),get_v(v['H市盈率动']),get_v(v['市净率']),get_v(v['涨停']),get_v(v['跌停'])
        )

    sql = insert_head + insert_list[:-1]
    cursor.execute(sql)
    db.commit()


def save_one_stock_exchange_data(db, code):

    exchange_data = 腾讯_个股当天交易数据(code)
    if not exchange_data:
        return None

    table_name = 't_day_{0}_exchange_{1}'.format(code,time.strftime('%Y_%m_%d', time.localtime(time.time())))
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `dbexchange`.`{0}`".format(table_name))

    # 使用预处理语句创建表
    sql = """CREATE TABLE `dbexchange`.`{0}` (
        `id` INT auto_increment NOT NULL,
        `时间` TIME NOT NULL,
        `成交价` FLOAT NOT NULL, 
        `价格变动` FLOAT NOT NULL, 
        `成交量手` FLOAT NOT NULL,
        `成交额元` FLOAT NOT NULL,
        `买卖方向` ENUM('B','S','M') DEFAULT 'M' NOT NULL,
        PRIMARY KEY (`id`))
        AUTO_INCREMENT = 0
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8;""".format(table_name)

    cursor.execute(sql)
    db.commit()

    insert_head = 'INSERT INTO `dbexchange`.`{0}` (`时间`, `成交价`,`价格变动`,`成交量手`,`成交额元`, `买卖方向`) VALUES'.format(table_name)
    insert_list = ""

    for i in exchange_data:
        insert_list += '''('{0}',{1},{2},{3},{4},'{5}'),'''.format(i[1],i[2],i[3],i[4],i[5],i[6])

    sql = insert_head + insert_list[:-1]
    cursor.execute(sql)
    db.commit()
    return True


def save_exchange_data(code_list):
    #code_list = 腾讯_获取A股股票代码(8000)
    db = pymysql.connect("localhost", "root", "000000")
    for i in code_list:
        t = save_one_stock_exchange_data(db, i)
        if not t:
            print("get code : {0} is failed".format(i))
        else:
            print("get code : {0} is success".format(i))
    db.close()

def multiprocess_save_exchange():
    '''
    开十个进程处理
    :return:
    '''
    p = Pool()
    code_list = 腾讯_获取A股股票代码(1000)

    code_list = list_nrow(code_list, 10)
    for i in code_list:
        print(i)
        p.apply_async(save_exchange_data, args = (i,))

    p.close()
    p.join()
    print('All subprocesses done.')

if __name__ == '__main__':
    # 打开数据库连接
    #db = pymysql.connect("localhost", "root", "000000")
    #log = print
    #create_table_by_execl(db, '2019-02-25.xls')

    #update_all_code_name_table(db)
    # update_all_code_name_table(db)
    #save_one_stock_exchange_data(db, '002678')

    #腾讯_获取多股实时基本数据信息(['600998'])
    # 关闭数据库连接
    #db.close()

    multiprocess_save_exchange()
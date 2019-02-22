import re,os,xlwt
from stock.tenxun.tenxun import *
from stock.tonghuashun.ths import *


finance_dir = "./data/stock/finance"
company_brief_dir = './data/stock/brief'

if __name__ == '__main__':

    # 上市年份列表 = {}
    # 过滤后的年份列表 = {}
    #
    #
    #
    # for file in os.listdir(company_brief_dir):
    #     file_path = os.path.join(company_brief_dir, file)
    #     if os.path.isfile(file_path):
    #         with open(file_path,'r',encoding='GBK') as f:
    #             str = f.read()
    #             f_str = re.search(r'上市日期：([0-9]*)',str)
    #             if f_str:
    #                 上市年份列表[file[:6]] = int(f_str.group(1))
    #
    # print(上市年份列表)
    #
    # for key,value in 上市年份列表.items():
    #     if value < 2015:
    #         过滤后的年份列表[key] = value
    #
    #
    # print(过滤后的年份列表)
    # #获取这些公司的财务数据，获取近三年 净利润同比增长率 都是增长的

    data_map = {}
    i = 0
    for file in os.listdir(finance_dir):
        code = file[:6]
        data = []
        isok = True

        file_data = 同花顺_获取公司单季度财务数据(code)

        if len(file_data[0]) < 17:
            continue

        for lv in file_data[3][1:12]:
            try:
                if lv == "--":
                    isok = False
                    break

                if float(lv[:-1]) < 10:
                    isok = False
                    break
            except Exception as err:
                raise Exception('file_data[3] = {0} \n lv = {1}, err= {2}, code = {3}'.format(file_data[3], lv,err,code))


        if isok:
            data.append(file_data[0][:12])
            data.append(file_data[3][:12])
            data_map[code] = data


    for key,value in data_map.items():
        print(key)
        print("    ",value[0])
        print("    ", value[1])

    for key in data_map.keys():
        if key[0] != '3':
            print(key)


    writebook = xlwt.Workbook()
    sheet = writebook.add_sheet('test')
    line = 0

    for key,value in data_map.items():

        sheet.write(line, 0, key)

        col = 1
        for v in value[0]:
            sheet.write(line, col, v)
            col = col + 1
        col = 1
        for v in value[1]:
            sheet.write(line + 1, col, v)
            col = col + 1
        line = line + 2

    writebook.save('answer.xls')


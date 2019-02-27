#!/usr/bin/python3
# encoding:utf-8
import os

def remov_dir(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            remov_dir(file_path)
        else:
            os.remove(file_path)

    os.rmdir(path)


def list_nrow(li, row):
    '''
    将一维数组，均分为 row 行的数组
    :param li: 一维列表；若传入的是多维列表，也只处理最外层的
    :param row: 需要装换成的行，即一维的元素个数
    :return:
    '''
    if row == 0:
        return None

    step = (len(li) + row - 1) // row

    return [li[i:i+step] for i in range(0, len(li), step)]
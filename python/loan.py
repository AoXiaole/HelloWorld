#!/usr/bin/python
import sys
# -*- coding: utf-8 -*-
def sum(li):
    su = 0

    for i in range(len(li)):
        su += li[i]
    return su

def 等额本息(本金, 月率, 期数):
    return (本金 * ((1+月率)**期数) * 月率) / ((1 + 月率) ** 期数 - 1 )



def 等额本金第i月的还款额(本金, 月率, 期数, i):
    return 本金 * ((1 + 月率 * ( 期数 - i + 1 )) / 期数 )

def 等额本金(本金, 月率, 期数):
    money_list = [0] * (期数 +1)
    for i in range(期数):
        money_list[i + 1] = 等额本金第i月的还款额(本金, 月率, 期数, i+1)

    return money_list[:]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("param len is not 3 ; {0}".format(sys.argv))

    本金 = float(sys.argv[1])
    年率 = float(sys.argv[2])
    期数 = int(sys.argv[3])

#30000, 0.05328 / 12, 12
    mm1 = 等额本息(本金, 年率 / 12, 期数)

    mm = 等额本金(本金, 年率 / 12, 期数)

    print("贷款金额 {0} 元，贷款 {1}% 年利率, 贷款分 {2} 期.".format(本金, 年率 * 100, 期数))
    print("还款方式一：等额本息")
    print("           每月还款 {0} 元".format(mm1))
    print("总额 {0} 元，总利息 {1} 元".format(mm1 * 期数, mm1 * 期数 - 本金))
    print("\n\n")
    print("还款方式一：等额本金")
    for i in range(期数):
        print("         第{0}期: {1}".format(i + 1, mm[i + 1]))
    print("         第{0}期: {1}".format(0 + 1, mm[0 + 1]))
    print("总额 {0} 元，总利息 {1} 元".format(sum(mm), sum(mm) - 本金))
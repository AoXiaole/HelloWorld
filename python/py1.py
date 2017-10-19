#!/bin/env python
# -*- coding: utf-8 -*-
# 任意无符号的对象，以逗号隔开，默认为元组
def nine_mul():
	for i in range(1,10):
		for j in range(1,i+1):
			print("%d*%d=%2d " % (j,i,i*j)),
		print

def myMethod(x,y):
	return x**y

def var_test():
	print "---string---"
	str1='nihao'
	print str1 * 2 #print second str1 
	print str1[1] 
	

	print "\n---列表 list---"
	li = ['runoob','786','2.234',1111]
	print li

	print "\n---元组 tuple---"	
	tup = (1,2,"345","hello")
	tup2 = ("tup2",4.567)
	print tup[1:3] 
	print tup+tup2


	print "\n---字典 dict---"
	dic={"name":"aao",'num':1234,"age":18}
	
	print dic
	print "name:",
	print dic['name'] 
	print "dic[age]:",
	print dic['age']
	print "keys:",
	print dic.keys()
	print "values:",
	print dic.values()


def var_test2():
	li=[1,2,3,4,5,6]
	li2=[11,22,33,44,55,66]
	dic={"name":"aoml",1:"1111","age":27}
	
	tup=(li,li2,dic)
		
	li2[2]=99

	print tup


def expr_test():
# Python运算符优先级
# 以下表格列出了从最高到最低优先级的所有运算符：
# 运算符	描述
# **		指数 (最高优先级)
# ~ + -		按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@)
# * / % //	乘，除，取模和取整除
# + -		加法减法
# >> <<		右移，左移运算符
# &			位 'AND'
# ^ |		位运算符
# <= < > >=	比较运算符
# <> == !=	等于运算符
# = %= /= //= -= += *= **=	赋值运算符
# is is not	身份运算符
# in not in	成员运算符
# not or and	逻辑运算符


# is 与 == 区别：
# is 用于判断两个变量引用对象是否为同一个， == 用于判断引用变量的值是否相等

	a=10
	b=60
	list=[10,20,30]
	list2=[10,20,30]
		
	if(a in list):
		print a," in ",list
	
	if(b not in list):
		print b,"not in ",list
	else:
		print b," in ",list
	b=10
	if(a is b):
		print "a is b",10,10
	if(list is list2):
		print "list1 is list"
	else:
		print "list is not list1"

	if(a/b == 1 and list):
		print "a/b =",a/b

	a=1
	b=0
	if not( a and b ):
		print "not (",a," and ",b," )"


def condition_test():
	flag=False #bool 
	name='luren'
	if name == 'python':
		flag=True
		print "welcome boss"
	elif name == 'aoml':
		flag=True
		print "welcome aoml"
	else:
		print "name is",name

	num=8
	if(num >= 0 and num <= 5) or(num >=10 and num <=15):print "hello ",num    #简单的语句可以写在一行
	else:
		print "num is ",num
	

def while_test():
	numbers=[12,37,5,42,8,3]
	even=[]
	odd=[]
	while len(numbers)>0:
		number=numbers.pop() #取出最后一个
		if(number % 2 == 0):
			even.append(number) #增加一个
		else:
			odd.append(number)
	print "even:",even
	print "odd :",odd
	

def tup_test():
	tup=("all",) # 括号既可以作为数学运算中的括号，也可以作为元组，所以当元组中只有一个元素的时候，需要增加一个逗号
	print tup

def dict_test():
# 键必须是不可变的，如字符串，数字或元组
	dict={1:'123',"a":'456',(1,2,3):{"d1":123,"tt":"qwer"}}
	print dict[(1,2,3)]['d1']
	print "keys:",dict.keys()
	print "values:",dict.values()



Money=2000
def AddMoney():
	global Money   # 全局变量需要使用global 说明，否则当局部变量处理
	Money = Money + 1
	print Money

	localList=locals()
	globalList=globals()
	
	print "localList:",localList
	print "globalList:",globalList
AddMoney()


#var_test2()
#expr_test()
#condition_test()
#dict_test()
	

	

#!/bin/env python
# -*- coding: UTF-8 -*-
def input_test():
	str=input("请输入一个表达式:");
	print "结果:",str

	str=raw_input("请输入一句话:");
	print "say:",str

def file_test1():
	fo = open("pyfile.test","a+")
	print "文件名:",fo.name
	
	fo.write("hahahahnihaohasdferrg\n"); #python write不会自动添加换行需要手动添加，pyton可以对二进制文件的读写

	position=fo.tell()  #获取当前位置
	print "当前文件位置:",position
	position = fo.seek(0,0) #移动文件到开头
	
	str=fo.read()  #read不指定长度的话则会自动尽可能多的读取，一般是从当前读到文件结尾
	print "file:",str

#input_test()
file_test1()

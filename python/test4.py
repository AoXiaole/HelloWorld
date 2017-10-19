#!/bin/env python
# -*- coding: UTF-8 -*-
months=[31,28,31,30,31,30,31,31,30,31,30,31]

year=int(raw_input("请输入年:"))

if(((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)):
	months[1]=29

while True:
	month=int(raw_input("请输入月:"))
	if ((month > 12) or (month < 1)):
		print "输入错误"
	else:
		break

while True:
	day=int(raw_input("请输入日:"))
	if ((day > months[month-1]) or (day < 0)):
		print "输入错误"
	else:
		break
	
	
days=0

for i in range(0,month-1):
	days += months[i]
days += day

print "it is the %dth day" % days

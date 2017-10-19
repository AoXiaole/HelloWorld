#!/bin/env python
# -*- coding: UTF-8 -*-
class Employee:
	'所有员工基类'
	empCount=0
	def __init__(self,name="name",salary=10000): #构造函数
		class_name=self.__class__.__name__
		print class_name,"创建"
		self.name=name	#self 实例本身，调用是不需要传，使用name初始化成员name
		self.salary=salary
		Employee.empCount +=1 #empCount 是 基类静态成员，所有基类的实例共享
	
	def __del__(self): #析构函数
		class_name=self.__class__.__name__
		print class_name,"销毁"

	def displayCount(self):
		print "Total Employee %d" % Employee.empCount
	def displayEmployee(self):
		print "Name: ",self.name," Salary: ",self.salary
	

def emplayee_test():
	"创建一个对象"
	emp1=Employee("Zara",2000)
	emp2=Employee("MMM",5000)

	emp1.displayEmployee()
	emp2.displayEmployee()

	emp2.displayCount()
	print "Total Employee %d" % Employee.empCount



	emp3=emp1 #增加引用,不会创建

	emp3.displayCount()
	print "del emp1"
	del emp1    #由于有其他引用，该对象实例没有删除，而是删除了一个引用

	emp3.displayCount()

class PPP(Employee):
	__private_var = "__private_var" #私有成员  __开头
	_protect_var = "_protect_var" #保护成员 _开头
	public_var = "public_var"
	PPP_var = 0

	def __init__(self):
	#	Employee.__init__() #子类初始化父类，需要手动调用构造函数
		PPP.PPP_var +=1
		print "PPP 创建"

	def __del__(self):
		PPP.PPP_var -=1
		print "PPP 销毁"
	
	def displayCount(self): #重写父类的函数
        	print "Total PPP %d" % PPP.PPP_var


def PPP_test():
	PPP1=PPP()
	PPP2=PPP()
	emp1 = Employee("ttt",20000)
	PPP1.displayCount()


PPP_test()

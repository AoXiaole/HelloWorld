#!/usr/bin/python 
# -*- coding: UTF-8 -*-
from numpy import *
import matplotlib
matplotlib.use('wx')
import matplotlib.pyplot as plt
#
X = array([ [1,1, 1],
			[1,1,3],
			[1,1,7],
			[1,3,1],
			[1,3,3],
			[1,3,7],
			[1,7,1],
			[1,7,7],
			[1,1,50],
			
			[1,-1, 1],
			[1,-1,3],
			[1,-1,7],
			[1,-3,1],
			[1,-3,3],
			[1,-3,7],
			[1,-7,1],
			[1,-7,7],
			[1,-1,50],
			
			[1,1, -1],
			[1,1,-3],
			[1,1,-7],
			[1,3,-1],
			[1,3,-3],
			[1,3,-7],
			[1,7,-1],
			[1,7,-7],
			[1,1,-50],
			
			[1,-1, -1],
			[1,-1,-3],
			[1,-1,-7],
			[1,-3,-1],
			[1,-3,-3],
			[1,-3,-7],
			[1,-7,-1],
			[1,-7,-7],
			[1,-1,-50],

			
			])
			  
D = array([	[1,1],
			[1,1],
			[1,1],
			[1,1],
			[1,1],
			[1,1],
			[1,1],
			[1,1],
			[1,1],
			
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			[-1,1],
			
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			[1,-1],
			
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],
			[-1,-1],

		])

W = array([ (random.random(3) - 0.5) * 2 , (random.random(3) - 0.5) * 2])

lr = 0.11

n = 0

O=zeros((D.shape),dtype=int16)
O_N= zeros((1,D.shape[1]),dtype=int16)
print "O_N = ",O_N



def cal(XN,Dj):
	global W,lr,O_N
	O_N = sign(XN.dot(W.T))
	W_C = lr * dot(matrix(Dj - O_N).T,matrix(XN))  #Dj 和 O_N ，XN 经过计算后都变成了数组，所以计算时需要转换为矩阵
	W = W + W_C         # W_C 的属性变成了 matrix ，所以 W的属性也跟着变，matrix 不能访问到具体元素，需要W.A 转化为数组才行
	

#for _ in range(10000):  #方法2 对X 一次计算，得到所有组的 (dalta)W，然后在取平均值，但效果却没有方法1 的计算次数少
#	n = n+1
#	O = sign(X.dot(W.T))
#	print "O=",O
#	if(O == D).all():
#		print("finished")
#		break
#	W_C = lr * dot(matrix(D - O).T,X)/X.shape[0]
#	W = W + W_C
	
for _ in range(10000): #方法1 X 一组一组的计算
	O=zeros((D.shape),dtype=int16)
	n = n+1
	for i in range(X.shape[0]):
		cal(X[i],D[i])
		O[i]=O_N

	if(O == D).all():
		print("finished")
		break

print "n = ",n

x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]
x4=[]
y4=[]

for i in range(X.shape[0]):
	if(D[i] == array([-1,-1])).all():
		x1.append(X[i][1])
		y1.append(X[i][2])
	elif(D[i] == array([-1,1])).all():
		x2.append(X[i][1])
		y2.append(X[i][2])
	elif(D[i] == array([1,-1])).all():
		x3.append(X[i][1])
		y3.append(X[i][2])	
	elif(D[i] == array([1,1])).all():
		x4.append(X[i][1])
		y4.append(X[i][2])

k0 = -W.A[0][1]/W.A[0][2]
d0 = -W.A[0][0]/W.A[0][2] 
k1 = -W.A[1][1]/W.A[1][2]
d1 = -W.A[1][0]/W.A[1][2] 


xdata = linspace(-50,50,2)

plt.figure()
plt.plot(xdata,xdata*k0 + d0, 'r')
plt.plot(xdata,xdata*k1 + d1, 'g')
plt.plot(x1,y1,'bo')
plt.plot(x2,y2,'yo')
plt.plot(x3,y3,'mo')
plt.plot(x4,y4,'ko')
plt.show()


			
			

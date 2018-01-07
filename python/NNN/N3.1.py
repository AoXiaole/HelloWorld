#!/usr/bin/python 
# -*- coding: UTF-8 -*-
from numpy import *
import matplotlib
matplotlib.use('wx')
import matplotlib.pyplot as plt
#
X = array([[1,2, 3],
			[1,2,5],
			[1,3,7],
			[1,6,9],
			[1,1,3],
			[1,4,8],
			[1,9,4],
			[1,6,2],
			[1,8,3]
			])
			  
D = array([ [1,1,1,1,1,1,-1,-1,-1] ])

W = array([ (random.random(3) - 0.5) * 2 ])

lr = 0.11

n = 0

o=0

def cal(XN,dj):
	global W,lr,o	
	o = sign(XN.dot(W.T))
	W_C = lr * (dj - o)* XN
	W = W + W_C
	
for _ in range(100):
	O = array([zeros(X.shape[0],dtype=int16)])
	n = n+1
	for i in range(X.shape[0]):
		cal(X[i],D[0][i])
		O[0][i]=o
		print W
	print "======>",W
	if(O == D).all():
		print("finished")
		break
		
	
print("hello n =%d",n)



x1=[]
y1=[]
x2=[]
y2=[]
for i in range(X.shape[0]):
	if(D[0][i] == 1):
		x1.append(X[i][1])
		y1.append(X[i][2])
	else:
		x2.append(X[i][1])
		y2.append(X[i][2])
		


k = -W[0][1]/W[0][2]
d = -W[0][0]/W[0][2] 
xdata = linspace(-15,15,2)

plt.figure()
plt.plot(xdata,xdata*k + d, 'r')
plt.plot(x1,y1,'bo')
plt.plot(x2,y2,'yo')
plt.show()


			
			

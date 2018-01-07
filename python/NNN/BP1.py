#!/usr/bin/python 
# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib
matplotlib.use('wx')
import matplotlib.pyplot as plt

#输入数据
X = np.array([[1,3,3],
	     [1,4,3],
	     [1,1,1]])

#输出
Y = np.array([1,1,-1])
#权值初始化，1行 3列 范围 -1到1

W = (np.random.random(3) - 0.5)*2
print(W)

#学习率设置
lr = 0.11

#计算次数
n = 0

#神经网络输出
O = 0

def update():
	global X,Y,W,lr,n,O
	n += 1
	O = np.sign(np.dot(X,W.T))
	W_C = lr * (( Y - O.T) .dot(X)) / int (X.shape[0])
	W = W + W_C

for _ in range(100)	:
	update()
	print(W)
	print(n)
	O = np.sign(np.dot(X,W.T))
	if(O == Y.T).all(): # 如果实际输出和期望输出一样，模型收敛
		print("Finished")
		print("epoch:",n)
		break
		
#正	
x1 = [3, 4]
y1 = [3, 3]

#负
x2 = [1]
y2 = [1]

k = -W[1]/W[2]
d = -W[0]/W[2] 
xdata = np.linspace(0,5)

plt.figure()
plt.plot(xdata,xdata*k + d, 'r')
plt.plot(x1,y1,'bo')
plt.plot(x2,y2,'yo')
plt.show()
	
	
	
	





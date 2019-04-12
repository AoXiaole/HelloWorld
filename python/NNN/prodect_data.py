import numpy as np
# n * 1 的矩阵
tw= np.array([2,3,4,5])
X= np.arange(1,17).reshape(4,4)
X[3,:] = 1


X2 = X.dot(X.T)

ww = np.random.random(4)

Y = tw.dot(X)

# print(X2)
# print(ww)
# print('\n')
# print(Y)
# print(ww.dot(2*X2) -Y.dot((2 * X).T))
#
# print('\n')


#
# def train(Wi):
#     print("Wi:",Wi)
#     fw = Wi.dot(2 * X2) - Y.dot((2 * X).T)
#     print("fw:",fw)
#     Wo = Wi - lr * fw
#
#     return Wo

#
# for i in range(10):
#
#     wout = train(ww)
#     if (wout == ww).all():  # 如果实际输出和期望输出一样，模型收敛
#         print("Finished")
#         print("epoch:", wout)
#         break
#     ww = wout
print("tw:\n", tw)
print("X:\n", X)
print("\n Y:\n",Y)

X1 = np.linalg.inv(X)

W= Y.dot(X1)
print("\nx1:\n",X1)

print("\nW:\n",W)

print("\nX*X1:\n",X.dot(X1))



# 方程式 y = 16x^3 + 18x^2 + 50x + 100
# -> y = w0 * x0 + w1 * x1 + w2 * x2 + w3
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


def produce_xDatayData():
    w = np.array([[100, 50, 18, 16]]).T
    x_data = np.random.uniform(-10, 10, size=(3, 1))
    x_data.sort(axis=0)
    # x_data = np.array([[1],[2],[3]])
    poly_reg = PolynomialFeatures(degree=3)
    x_poly = poly_reg.fit_transform(x_data)
    y_data = x_poly.dot(w)
    # print(y_data)
    #g = np.random.uniform(-0.1, 0.1, size=(3, 1))
    #y_data = y_data - g
    #print("y_data:",y_data)
    return x_data, y_data


def combination(li,n):
    com = []
    if n == 1:
        for i in li:
            com.append([i])
        return com
    if n >= len(li):
        com.append(li)
    for i in range(len(li[:1-n])):
        tmp = combination(li[1+i : ],n-1)
        for j in tmp:
            cl = [li[i]] + j
            com.append(cl)
    return com

x_data , y_data = produce_xDatayData()

m = float(len(x_data))

poly_reg = PolynomialFeatures(degree=3)
x_poly = poly_reg.fit_transform(x_data)

w = np.linalg.inv(x_poly.T.dot(x_poly)).dot(x_poly.T).dot(y_data)
print(w)

plt.plot(x_data, y_data, 'b.')

plt.plot(x_data, x_poly.dot(w), 'r')
plt.show()
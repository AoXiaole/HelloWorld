# 方程式 y = 17x^4+16x^3 + 18x^2 + 50x + 100
#-> y = w0 * x0 + w1 * x1 + w2 * x2 + w3
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

def produce_xDatayData():
    w = np.array([[100,50,18,16,17]]).T
    x_data = np.random.uniform(-10,10,size=(500,1))
    x_data.sort(axis=0)
    #x_data = np.array([[1],[2],[3]])
    poly_reg = PolynomialFeatures(degree=4)
    x_poly = poly_reg.fit_transform(x_data)
    y_data = x_poly.dot(w)
    # print(y_data)
    g =  np.random.uniform(-100,100,size=(500,1))
    y_data = y_data - g
    # print("y_data:",y_data)
    return x_data,y_data

def loss(x_poly, y_data, w):
    y_predict = x_poly.dot(w)
    y_ss = (y_predict - y_data) ** 2
    y_loss = y_ss.sum() / len(y_data) / 2
    return y_loss

def D_value_sum(x_poly,w,y_data):
    y_predict = x_poly.dot(w)
    y_sum = y_predict - y_data

    return y_sum.sum()

lr = 0.0000001
x_data , y_data = produce_xDatayData()
w = np.array([[0,0,0,0,0]]).T
m = float(len(x_data))

poly_reg = PolynomialFeatures(degree=4)
x_poly = poly_reg.fit_transform(x_data)
f_w = np.zeros((5,1))

print("x_data:\n",x_data)
print("y_data:\n",y_data)
print("w:\n",w)
print("x_poly:\n",x_poly)
plt.plot(x_data,y_data,'b.')
plt.show()

for k in range(10000):

    for j in range(len(w)):
        f_w[j][0] = 0
        for i in range(len(x_data)):
            f_w[j][0] += (x_poly[i].dot(w) - y_data[i]) * x_poly[i][j]


    w = w - lr * f_w / m
    print("f_w/m:\n", f_w/m)
    print("w:\n",w)
    print("loss:\n",loss(x_poly,y_data,w))


    if k % 1000 == 0:
        plt.plot(x_data,y_data,'b.')

        plt.plot(x_data, x_poly.dot(w), 'r')
        plt.show()




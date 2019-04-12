import numpy as np
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
# 读入数据 \n
w = []
def slearn_fun():
    data = np.loadtxt("a.csv")

    #plt.scatter(x_data,y_data)
    x_data = data[:,0,np.newaxis]
    y_data = data[:,1,np.newaxis]
    # 创建并拟合模型
    model = LinearRegression()
    model.fit(x_data, y_data)
    plt.plot(x_data, y_data, 'b.')

    poly_reg  = PolynomialFeatures(degree=4)
    x_poly = poly_reg.fit_transform(x_data)
    #print(x_poly)
    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, y_data)

    plt.plot(x_data, lin_reg.predict(poly_reg.fit_transform(x_data)), c='r')

    print(lin_reg.coef_)

    w = lin_reg.coef_
    print(lin_reg.intercept_)
    plt.show()


def 标准方程():
    data = np.loadtxt("a.csv")
    x_data = data[:, 0, np.newaxis]
    y_data = data[:, 1, np.newaxis]
    #print(x_data)
    #print(y_data)
    poly_reg = PolynomialFeatures(degree=4)
    x_poly = poly_reg.fit_transform(x_data)
    global w
    w = np.linalg.inv(x_poly.T.dot(x_poly)).dot(x_poly.T).dot(y_data)
    print(w)
def 测试(x_data):

    poly_reg = PolynomialFeatures(degree=4)
    x_t = np.array(x_data)
    x_t.shape = (len(x_data),1)
    x_poly = poly_reg.fit_transform(x_t)
    print(x_poly)
    y = x_poly.dot(w)
    print(y)
标准方程()



slearn_fun()

测试([1,2,3,4,5,2000,3000,4000,5000])


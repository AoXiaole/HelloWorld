import tensorflow as tf

# 获取默认的数据流图
default_graph = tf.get_default_graph()

# 创建了一个新的数据流图
g = tf.Graph()

with default_graph.as_default(): #默认的数据流图定义
    a = tf.constant(5, name = "input_a")
    b = tf.constant(6, name = "input_b")
    c = tf.multiply(a, b, name = "mul")
    d = a * c   # 已经重载了 * 的基本运算符

    e = tf.constant([5,3], name="input_a")
    e1 = tf.reduce_prod(e, name="prod_b") # 对张量的所有分量进行相乘处理
    e2 = tf.reduce_sum(e, name ="sum_e")

with g.as_default():
    a1 = tf.constant(5, name="input_a")
    b1 = tf.constant(6, name="input_b")
    c1 = tf.multiply(a, b, name="mul")
    d1 = a1 * c1  # 已经重载了 * 的基本运算符

    e01 = tf.constant([5, 3], name="input_a")
    e11 = tf.reduce_prod(e, name="prod_b")  # 对张量的所有分量进行相乘处理
    e21 = tf.reduce_sum(e, name="sum_e")



# 默认是执行默认的数据流图，也可以通过graph来指定
sess = tf.Session(graph=default_graph)
v_t = sess.run(c)
v_d = sess.run(d)
writer =  tf.summary.FileWriter('./HH', sess.graph)
writer.close()
sess.close()
print(v_t)
print(v_d)

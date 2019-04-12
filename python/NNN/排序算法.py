
import random

a = [random.randint(1,100) for _ in range(100) ]
print(a)

# 冒泡排序

def 选择排序(a):
    '''
    从小到大排序，假设序号i前有序，后面无序，那么从第i到最后数之间选择一个最小的放在第i的位置。然后i后移
    算法分析，每次选择最小值，都需要不断的更新m,但列表的交换次数很少，
    :param a:
    :return:
    '''
    len_a = len(a)

    for i in range(len_a-1):
        m = i
        for j in range(i+1, len_a):
            if a[m] > a[j]:
                m = j
        a[m],a[i] = a[i],a[m]  # 因为是数值，不是引用，所以可以这样直接交换


def 冒泡排序(a):
    '''
    从小到大排序，假设序号i前无序，后有序；那么从0开始，将数据大的数据向上冒泡，直到送到第i-1的位置
    算法分析，排序过程中已经将较大的数据往后排，会一定的减少后面排序的交换次数
    :param a:
    :return:
    '''
    len_a = len(a)
    for i in range(len_a-1):
        for j in range(len_a-i-1):
            if a[j] > a[j+1]:
                a[j],a[j+1] = a[j+1],a[j]
    


def 插入排序(a):
    '''
    从小到大的排序，假设序号i前是有序的，i之后是无序的，那么选择i+1,依次从 i-0 比较，当发现k的数比他小时，
    则将该值插入到k值的后面，原来k+1到i的元素向后移一个单位
    :param a:
    :return:
    '''
    len_a = len(a)
    for i in range(1,len_a):

        for j in range(i-1,-1,-1):
            if a[j]  > a[j+1]:
                a[j],a[j+1] = a[j+1],a[j]
            else:
                break




def 归并排序(a):
    '''
    1.把长度为n的输入序列分成两个长度为n/2的子序列
    2.对这两个子序列分别采用归并排序
    3.将两个排序好的子序列合并成一个最终的排序序列

    :param a:
    :return:
    '''

    len_a = len(a)
    if len_a == 0:
        raise Exception("error")
    if len_a == 1:
        return a
    if len_a == 2:
        if a[0]>a[1]:
            a[0],a[1] = a[1],a[0]
        return a
    else:
        left = 归并排序(a[:len_a//2])
        right = 归并排序(a[len_a//2:])

    i = 0
    j = 0
    k=0
    left_len = len(left)
    right_len = len(right)
    while True:
        if left[i] < right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        k += 1

        if i == left_len:
            a[k:] = right[j:]
            break
        if j == right_len:
            a[k:] =left[i:]
            break
    #print("left+ right :",a)
    return a


def 快速排序(a):

    if len(a) == 0:
        raise Exception("ERROR")
    if len(a) == 1:
        return a
    if len(a) == 2:
        if a[0]>a[1]:
            a[0] , a[1] = a[1],a[0]
        return a

    b = a[0]
    i = 0
    j = len(a) -1

    while True:
        while i < j and a[j] >= b:
            j = j - 1
        while i < j and a[i] <= b:
            i = i + 1
        if i == j:
            a[i],a[0] = a[0],a[i]
            #print("交换base：",a)
            if i != 0:
                left = 快速排序(a[:i])
                a[:i] = left
            if i != len(a)-1:
                right = 快速排序(a[i+1:])
                a[i+1:] = right
            break
        else:
            a[i],a[j] = a[j],a[i]
            #print("交换{0},{1}:".format(i,j), a)

    return a

b1 = a[:]
b2 = a[:]
b3 = a[:]
b4 = a[:]
b5 = a[:]

选择排序(b1)
print("选择排序\n",b1)

冒泡排序(b2)
print("冒泡排序\n",b2)

插入排序(b3)
print("插入排序\n",b3)

归并排序(b4)
print("归并排序\n",b4)

快速排序(b5)
print("快速排序\n",b5)





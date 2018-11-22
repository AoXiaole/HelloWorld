import requests
from pyquery import PyQuery as pq
from mm.stock_list import *
p_get=requests.get('http://gu.qq.com/sh600436/gp')
print(p_get.text)

doc = pq(p_get.text)
items = doc("tr.tron")

codec_list={}
for item in stock_list_day_data:
    codec_list[item[1]]= item[2]



print(items)
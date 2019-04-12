import requests,json
import numpy as np
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
url = 'http://www.zhishuchacha.com/getdata.php'
d = {"val[]": 5000, "type": "jyzs"}
#r = requests.post(url,headers=headers, data=d)
#print(r.text)

def 交易金额(e):
    global d
    d["val[]"] = e
    r = requests.post(url,headers=headers, data=d)
    js = json.loads(r.text)
    return js.get("data")[0]


data = []

for i in range(20000, 400000, 2000):

    v = 交易金额(i)
    print(i,v)
    a = []
    a.append(i)
    a.append(v)
    data.append(a)

da = np.array(data)
print(da)
np.savetxt('a.csv', da)

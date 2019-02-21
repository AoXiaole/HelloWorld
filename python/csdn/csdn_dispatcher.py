import socket,threading,json
from mymodule.csdn_config import *

# 接受web服务器发送来的socket请求，然后根据请求分发到不同的CSDN账号对应的下载器

def recv_down_request(ip,port):
    # 开启ip和端口
    ip_port = (ip, port)
    # 生成句柄
    web = socket.socket()
    # 绑定端口
    web.bind(ip_port)
    # 最多连接数
    web.listen(5)
    # 等待信息
    print('waiting...')
    #开启死循环
    while True:
        #阻塞
        conn,addr = web.accept()
        #获取客户端请求数据
        data = conn.recv()
        #打印接受数据 注：当浏览器访问的时候，接受的数据的浏览器的信息等。

        # 通过data得到url
        data_dict = json.dumps(data)
        url = data_dict.get('url','')
        if not url:
            m_down_thread = threading.Thread(target=download,args=(url,))
            m_down_thread.start()

        print(data)
        #向对方发送数据
        conn.send(bytes('geurl ok','utf8'))
        #关闭链接
        conn.close()

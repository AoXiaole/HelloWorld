
# !/usr/bin/env python
# coding:utf-8
import socket
import threading

# V1 版本先实现一个内网服务器的穿透
#1 监听 bind_port = 7000 端口，等待 内网服务器的连接

#2. 监听 vhost_http_port = 6081 端口，等待客户端浏览器的连接
host_ip = '183.15.178.247'
bind_port = 7000
vhost_http_port = 6081


def accept_thread(port,new_socket_deal):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip,port))
    sock.listen(15)
    while True: #循环轮询socket状态，等待访问
        connection,address = sock.accept()
        try:
            connection.settimeout(50)
            print("have a new client",address)
            #获得一个连接，然后开始循环处理这个连接发送的信息
            '''''
            如果server要同时处理多个连接，则下面的语句块应该用多线程来处理，
            否则server就始终在下面这个while语句块里被第一个连接所占用，
            无法去扫描其他新连接了，但多线程会影响代码结构，所以记得在连接数大于1时
            下面的语句要改为多线程即可。
            '''
            new_thread = threading.Thread(target=new_socket_deal, args=(connection,))
            new_thread.start()

        except socket.timeout: #如果建立连接后，该连接在设定的时间内无数据发来，则time out
             print('time out')


def new_http_socket(connection):
    client = connection

    buf = client.recv(2048)

    client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    client.send("Hello, World".encode())
    client.close()


if __name__ == '__main__':
   accept_thread(7000,new_http_socket)
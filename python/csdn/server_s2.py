#!/usr/bin/python3
# coding:utf-8
import socket,re,time,sys

def recv_thread(sockfd):
    pass

s2_ip = "193.112.143.47"
s2_port = 8877
server_ip = "118.25.239.224"

server_port = 8877
sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockfd.bind(('', 8877))

msg, addr = sockfd.recvfrom(1024)

print(msg.decode('utf-8'), addr)

client_ip,port= msg.split(" ")

print("client_ip:", client_ip)
print("port:",port)
#去连接客户端

sockfd.sendto("nihao".encode('utf-8'), (client_ip, int(port)))

sockfd.close()
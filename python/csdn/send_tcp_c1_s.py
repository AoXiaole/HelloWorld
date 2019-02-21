#!/usr/bin/python3
# coding:utf-8
import socket,re,time,sys

s2_ip = "193.112.143.47"
s2_port = 8877
server_ip = "118.25.239.224"

server_port = 8877

print("\n")

sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sockfd.bind(('', 3456))


sockfd.sendto("nihao".encode('utf-8'), (server_ip, server_port))


msg, addr = sockfd.recvfrom(1024)
print(msg.decode('utf-8'), addr)

clientip, strport = msg.decode('utf-8').split(";")
clientport=int(strport)

print("clientip:", clientip)
print("clientport:", clientport)

sockfd.sendto("nihao my is c1".encode('utf-8'), (clientip, clientport))

msg, addr = sockfd.recvfrom(1024)
print(msg.decode('utf-8'), addr)
print("finish")
#sockfd.close()

sockfd_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd_tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sockfd_tcp.bind(('', 3456))
sockfd_tcp.listen(5)

conn,addr = sockfd_tcp.accept()
data = conn.recv(1024)
print(data)
conn.send("i have get you message".encode('utf-8'))
conn.close()

sockfd_tcp.close()
#!/usr/bin/python3
# coding:utf-8
import socket,re,time,sys

s2_ip = "193.112.143.47"
s2_port = 8877
server_ip = "118.25.239.224"

server_port = 8877

print("\n")

# sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# sockfd.bind(('', 3456))
#
#
# sockfd.sendto("nihao".encode('utf-8'), (server_ip, server_port))
#
#
# msg, addr = sockfd.recvfrom(1024)
# print(msg.decode('utf-8'), addr)
#
#
# clientip, strport = msg.decode('utf-8').split(";")
# clientport=int(strport)
#
# print("clientip:", clientip)
# print("clientport:", clientport)
#
#
# sockfd_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sockfd_tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# sockfd_tcp.bind(('', 3456))
# time.sleep(1)
#
# sockfd_tcp.connect((server_ip, server_port))
#
# sockfd_tcp.sendall("hello".encode('utf-8'))
#
# data = sockfd_tcp.recv(1024)
# print(data)
# sockfd_tcp.close()

sockfd_tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd_tcp2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sockfd_tcp2.settimeout(1)
sockfd_tcp2.bind(('', 3456))

sockfd_tcp2.connect((server_ip, s2_port))

sockfd_tcp2.sendall("hello".encode('utf-8'))

data = sockfd_tcp2.recv(1024)
print(data)


sockfd_tcp2.connect((server_ip, s2_port))

sockfd_tcp2.sendall("hello".encode('utf-8'))

data = sockfd_tcp2.recv(1024)
print(data)

sockfd_tcp2.close()
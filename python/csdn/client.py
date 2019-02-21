#!/usr/bin/python3
# coding:utf-8
import socket,re,time,sys

# 接受码
class CODE:
    MSG_S1 = "msg_s1"
    MSG_OTHER_PROCESS = ""
    MSG_S1_OHTER_SOCK = "msg_s1_other_sock"
    MSG_S1_OHTER_PORT = "msg_s1_other_port"
    MSG_S2 = "msg_s2"

def recv_thread(sockfd):
    pass

s2_ip = "193.112.143.47"
s2_port = 8877
server_ip = "118.25.239.224"

server_port = 8877
sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sockfd.bind(('', 3456))

sockfd2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockfd2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sockfd2.bind(('', 3456))

sockfd.sendto("nihao".encode('utf-8'), (server_ip, server_port))
sockfd2.sendto("nihao".encode('utf-8'), (s2_ip, s2_port))
while True:
    msg, addr = sockfd.recvfrom(1024)
    print(msg.decode('utf-8'), addr)
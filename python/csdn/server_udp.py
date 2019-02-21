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

msg, addr1 = sockfd.recvfrom(1024)

print(msg.decode('utf-8'), "addr1:", addr1, "\n")

msg, addr2 = sockfd.recvfrom(1024)

print(msg.decode('utf-8'), "addr1:", addr2, "\n")


msg_addr1 = addr1[0] + ";" + str(addr1[1]) + "\n"
msg_addr2 = addr2[0] + ";" + str(addr2[1]) + "\n"

sockfd.sendto(msg_addr1.encode('utf-8'), addr2)
sockfd.sendto(msg_addr2.encode('utf-8'), addr1)

sockfd.close()
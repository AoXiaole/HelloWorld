# -*- coding: utf-8 -*-
from csdn.csdn_dower import *
import itchat
import pprint
from itchat.content import *


itchat.auto_login(hotReload=True)

@itchat.msg_register(TEXT)
def simple_reply(msg):
    #pprint.pprint(msg)
    bsType,*param= msg['Text'].split(" ")
    if bsType == 'CSDN下载':
        msg.user.send("文件下载中...")
        csdner = CSDN()
        file = csdner.csdn_download(*param)
        if not file:
            return 'download failed'
        print("send ",'@fil@{0}'.format(file), msg['FromUserName'])
        msg.user.send("文件上传中...")
        msg.user.send('@fil@{0}'.format(file))
        return '文件下载完成'


itchat.run()
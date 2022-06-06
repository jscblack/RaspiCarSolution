'''
Author       : Gehrychiang
LastEditTime : 2022-06-06 15:46:30
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
#用于向客户端发送消息
import socket
server = socket.socket()
server.bind(('127.0.0.1', 18080))
server.listen(5)
while True:
    try:
        conn, client_addr = server.accept()
        print('客户端已连接')
        while True:
            try:
                data = conn.recv(512)
                print('已收到客户端信息：', data.decode('utf-8'))
                if len(data)==0:
                    conn.close()
                    break
            except ConnectionResetError:
                print('连接断开')
                conn.close()
                break
    except Exception:
        print('监听终止')
        break
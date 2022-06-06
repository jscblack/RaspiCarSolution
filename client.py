'''
Author       : Gehrychiang
LastEditTime : 2022-06-06 22:07:23
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
#客户端
import socket
import threading
import cv2
import numpy as np
import time
# config area
vid_port=18081
cmd_port=18082
localhost='127.0.0.1'
ip_addr=localhost
# config end

def vid_downstream():
    while True:
        client = socket.socket()
        client.connect((ip_addr, vid_port))
        print('服务端已连接')
        while True:
            try:
                res=client.recv(131072)
                # print('已收到服务器信息：', res.decode('utf-8'))
                # res=client.recv(1024)
                print('received',len(res))
                nparr = np.frombuffer(res, dtype='uint8')
                im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow('client_test',im)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):  # q键推出
                    break
            except ConnectionResetError:
                print('连接断开，等待重新连接')
                client.close()
                break
            except Exception:
                print('连接终止，尝试重启')
                break

def cmd_upstream():
    while True:
        client = socket.socket()
        client.connect((ip_addr, cmd_port))
        print('服务端已连接')
        while True:
            try:
                # cmd is a json string
                # {'cmd':'move','para':{'direction':'forward','speed':'0.5'}}
                # {'cmd':'getStatus','para':{}}
                # cmd_exp='{"cmd":"getStatus","para":{}}'
                cmd_exp='cmd_exp_exp'
                print('发送命令：',cmd_exp)
                client.send(cmd_exp,encoding='utf-8')

                # ret=client.recv(65535)
                # print('响应结果 ',ret.decode('utf-8'))
                time.sleep(1)

            except ConnectionResetError:
                print('连接断开，等待重新连接')
                client.close()
                break
            except Exception:
                print('连接终止，尝试重启')
                break
    
if __name__ == "__main__":
    # vid_thread = threading.Thread(target=vid_downstream)
    # vid_thread.start()
    cmd_upstream=threading.Thread(target=cmd_upstream)
    cmd_upstream.start()
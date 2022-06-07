'''
Author       : Gehrychiang
LastEditTime : 2022-06-07 12:47:44
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import threading
import socket
import time
import cv2
from PIL import ImageGrab
import numpy as np
import json
import struct
# config area
vid_port=18081
cmd_port=18082
localhost='127.0.0.1'
ip_addr=localhost
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
# config end

def vid_upstream():
    while True:
        server = socket.socket()
        server.bind((ip_addr, vid_port))
        server.listen(5)
        print('服务端开启监听')
        while True:
            try:
                conn, client_addr = server.accept()
                print('客户端已连接')
                while True:
                    try:
                        im=ImageGrab.grab((0,0,854,480))
                        trans_cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2RGBA)# for display
                        # cv2.imshow('server_test',trans_cv2img)
                        # key = cv2.waitKey(1) & 0xFF
                        # if key == ord('q'):  # q键推出
                        #     break
                        # !!get a cv mat above!!

                        im_encode=cv2.imencode('.jpg',trans_cv2img)[1]
                        data_encode = np.array(im_encode)
                        str_encode = data_encode.tobytes()
                        conn.send(str_encode)
                        # print('sent',len(str_encode))
                        time.sleep(0.016) # 60fps

                    except ConnectionResetError:
                        print('连接断开，等待重新连接')
                        conn.close()
                        break
            except Exception:
                print('监听终止，尝试重启')
                break

def get_status():
    return "i am ok"

def cmd_downstream():
    while True:
        server = socket.socket()
        server.bind((ip_addr, cmd_port))
        server.listen(5)
        print('服务端开启监听')
        while True:
            try:
                conn, client_addr = server.accept()
                print('客户端已连接')
                while True:
                    try:
                        req=conn.recv(512)
                        req_prased=json.loads(req.decode('utf-8'))
                        print('解析请求：',req_prased["cmd"])
                        # if req_prased["cmd"]=='getStatus':
                        #     res=get_status()
                        #     ret_d=json.dumps({"ret":200,"data":{"status":res}})
                        #     print(ret_d)
                        #     conn.send(ret_d.encode('utf-8'))

                    except ConnectionResetError:
                        print('连接断开，等待重新连接')
                        conn.close()
                        break
            except Exception:
                print('监听终止，尝试重启')
                break



# def sec_thread_func():
#     # TODO

# def thd_thread_func():
#     # TODO

if __name__ == "__main__":
    vid_thread = threading.Thread(target=vid_upstream)
    vid_thread.start()
    # vid part is done 2022年6月7日09:55:24
    
    cmd_thread = threading.Thread(target=cmd_downstream)
    cmd_thread.start()
    # cmd part is done 2022年6月7日10:17:46

    # sec_thread = threading.Thread(target=sec_thread_func)
    # thd_thread = threading.Thread(target=thd_thread_func)
    # sec_thread.start()
    # thd_thread.start()
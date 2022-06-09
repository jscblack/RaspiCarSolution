'''
Author       : Gehrychiang
LastEditTime : 2022-06-09 11:44:07
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import socket
import time
import cv2
import numpy as np
import json
import multiprocessing
from multiprocessing import shared_memory
from loguru import logger
import camera
import fire_recog

# config area
vid_port = 18081
cmd_port = 18082
localhost = '127.0.0.1'
remotehost = '192.168.1.101'
ip_addr = localhost
encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 75]

# config end


def vid_upstream(arr_name):
    shm_ghost = shared_memory.SharedMemory(name=arr_name)
    arr = np.ndarray(shape=(480, 854, 3), dtype=np.uint8, buffer=shm_ghost.buf)
    while True:
        server = socket.socket()
        server.bind((ip_addr, vid_port))
        server.listen(5)
        logger.debug('<视频> 服务端开启监听'+' '+str(ip_addr)+':'+str(vid_port))
        while True:
            try:
                conn, client_addr = server.accept()
                logger.debug('<视频> 客户端已连接'+' '+str(client_addr))
                while True:
                    try:
                        trans_cv2img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGBA)
                        # trans_cv2img = cv2.resize(
                        #     trans_cv2img, dsize=[854, 480])
                        # print(len(trans_cv2img.tobytes()))
                        # cv2.imshow('server_test',trans_cv2img)
                        # key = cv2.waitKey(1) & 0xFF
                        # if key == ord('q'):  # q键退出
                        #     break
                        # !!get a cv mat above!!
                        im_encode = cv2.imencode('.WEBP', trans_cv2img,
                                                 encode_param)[1]
                        data_encode = np.array(im_encode)
                        str_encode = data_encode.tobytes()
                        conn.send(str_encode)
                        # print(len(str_encode))
                        # print('sent',len(str_encode))
                        time.sleep(0.015)  # 60fps this can be adjusted

                    except ConnectionResetError:
                        logger.error('<视频> 连接断开，等待重新连接')
                        conn.close()
                        break
            except Exception:
                logger.error('<视频> 监听终止，尝试重启')
                break


def get_status():
    # 随机返回一个温湿度
    return json.dumps({
        "temp": np.random.randint(20, 30),
        "humi": np.random.randint(40, 60)
    })


def cmd_downstream():
    while True:
        server = socket.socket()
        server.bind((ip_addr, cmd_port))
        server.listen(5)
        logger.debug('<指令> 服务端开启监听'+' '+str(ip_addr)+':'+str(cmd_port))
        while True:
            try:
                conn, client_addr = server.accept()
                logger.debug('<指令> 客户端已连接'+' '+str(client_addr))
                while True:
                    try:
                        req = conn.recv(512)
                        req_prased = json.loads(req.decode('utf-8'))
                        logger.debug('<指令> 请求解析'+' '+str(req_prased))
                        if req_prased["cmd"] == 'ping':
                            ret_d = json.dumps({"ret": 200, "data": "pong"})
                            conn.send(ret_d.encode('utf-8'))
                        elif req_prased["cmd"] == 'envStatus':
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": get_status()
                            })
                            conn.send(ret_d.encode('utf-8'))
                        elif req_prased["cmd"] == 'move':
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to move!'
                            })
                            conn.send(ret_d.encode('utf-8'))
                        elif req_prased["cmd"] == 'chmod':
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to change my mode'
                            })
                            conn.send(ret_d.encode('utf-8'))
                        elif req_prased["cmd"] == 'stop':
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to stop!'
                            })
                            conn.send(ret_d.encode('utf-8'))
                        else:
                            ret_d = json.dumps({
                                "ret": 404,
                                "data": "not complete"
                            })
                            conn.send(ret_d.encode('utf-8'))

                    except ConnectionResetError:
                        logger.error('<指令> 连接断开，等待重新连接')
                        conn.close()
                        break
            except Exception:
                logger.error('<指令> 监听终止，尝试重启')
                break


if __name__ == "__main__":
    cam_shm = shared_memory.SharedMemory(
        create=True, size=854 * 480 * 3)  # used for cam share
    cam_main = multiprocessing.Process(
        target=camera.camera_capture, args=(cam_shm.name, ), daemon=True)
    logger.debug('启动摄像头进程')
    cam_main.start()

    vid_process = multiprocessing.Process(
        target=vid_upstream, args=(cam_shm.name, ), daemon=True)
    vid_process.start()
    cmd_process = multiprocessing.Process(target=cmd_downstream, daemon=True)
    cmd_process.start()
    '''
    fire_que = multiprocessing.Queue()

    fire_process = multiprocessing.Process(
        target=fire_recog.predict_fire,
        args=(cam_shm.name, fire_que),
        daemon=True)
    '''
    # kill process
    cam_main.join()
    vid_process.join()
    cmd_process.join()

    def on_closing():
        cam_main.terminate()
        vid_process.terminate()
        cmd_process.terminate()
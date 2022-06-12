'''
Author       : Gehrychiang
LastEditTime : 2022-06-12 16:11:39
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import socket
import time
import cv2
import numpy as np
import json
import multiprocessing
from loguru import logger
import car

# config area
cmd_port = 18082
localhost = '127.0.0.1'
remotehost = '192.168.1.102'
ip_addr = remotehost
encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 75]
# config end

def get_status():
    # 随机返回一个温湿度
    return json.dumps({
        "temp": np.random.randint(20, 30),
        "humi": np.random.randint(40, 60)
    })


def cmd_downstream(cmd2car_que):
    while True:
        server = socket.socket()
        server.bind((ip_addr, cmd_port))
        server.listen(5)
        logger.debug('<指令> 服务端开启监听' + ' ' + str(ip_addr) + ':' + str(cmd_port))
        while True:
            try:
                conn, client_addr = server.accept()
                logger.debug('<指令> 客户端已连接' + ' ' + str(client_addr))
                while True:
                    try:
                        req = conn.recv(512)
                        req_prased = json.loads(req.decode('utf-8'))
                        req_data=req_prased["para"]
                        
                        logger.debug('<指令> 请求解析' + ' ' + str(req_prased))
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
                            if req_data["direction"] == 'forward':
                                cmd2car_que.put(1)
                            elif req_data["direction"] == 'backward':
                                cmd2car_que.put(2)
                            elif req_data["direction"] == 'left':
                                cmd2car_que.put(3)
                            elif req_data["direction"] == 'right':
                                cmd2car_que.put(4)

                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to move!'
                            })
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'chmod':
                            if req_data["to"] == 'manual':
                                cmd2car_que.put(5)
                            elif req_data["to"] == 'auto-lane':
                                cmd2car_que.put(6)
                            elif req_data["to"] == 'auto-avoidance':
                                cmd2car_que.put(7)

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
    # localIP = socket.gethostbyname(socket.gethostname())
    # ip_addr = localIP
    # logger.debug('本机IP为' + ' ' + ip_addr)
    
    cmd2car_que = multiprocessing.Queue()

    cmd_process = multiprocessing.Process(
        target=cmd_downstream, args=(cmd2car_que, ), daemon=True)
    cmd_process.start()

    car_process = multiprocessing.Process(
        target=car.car_main, args=(cmd2car_que,), daemon=True)
    car_process.start()
    '''
    fire_que = multiprocessing.Queue()

    fire_process = multiprocessing.Process(
        target=fire_recog.predict_fire,
        args=(cam_shm.name, fire_que),
        daemon=True)
    '''

    # kill process
    cmd_process.join()
    car_process.join()

    def on_closing():
        cmd_process.terminate()
        car_process.terminate()
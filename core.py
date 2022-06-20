'''
Author       : Gehrychiang
LastEditTime : 2022-06-20 17:10:13
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import socket
import json
import multiprocessing
from loguru import logger
import car
import env
import sys
# config area
vid_port = 18081
cmd_port = 18082
localhost = '127.0.0.1'
remotehost = '192.168.1.102'
anyhost = '0.0.0.0'
ip_addr = anyhost
# config end

def cmd_downstream(cmd2car_que,sensor2cmd_que):
    while True:
        server = socket.socket()    
        server.bind((ip_addr, cmd_port))
        server.listen(5)
        logger.info('<指令> 服务端开启监听' + ' ' + str(ip_addr) + ':' + str(cmd_port))
        cache_temp=0
        cache_humd=0
        cache_fire=0
        while True:
            try:
                conn, client_addr = server.accept()
                logger.info('<指令> 客户端已连接' + ' ' + str(client_addr))
                while True:
                    try:
                        req = conn.recv(512)
                        req_prased = json.loads(req.decode('utf-8'))
                        req_data = req_prased["para"]
                        logger.debug('<指令> 请求解析' + ' ' + str(req_prased))
                        if req_prased["cmd"] == 'ping':
                            ret_d = json.dumps({"ret": 200, "data": "pong"})
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'envStatus':
                            if not sensor2cmd_que.empty():
                                cache_temp,cache_humd,cache_fire = sensor2cmd_que.get()
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": json.dumps({
                                    "temp": cache_temp,
                                    "humi": cache_humd,
                                    "fire": cache_fire,
                                    })
                            })
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'move':
                            if req_data["direction"] == 'forward':
                                if req_data["behavior"] == 'accelerate':
                                    cmd2car_que.put(1)
                                else:
                                    cmd2car_que.put(5)
                            elif req_data["direction"] == 'backward':
                                if req_data["behavior"] == 'accelerate':
                                    cmd2car_que.put(2)
                                else:
                                    cmd2car_que.put(6)
                            elif req_data["direction"] == 'left':
                                if req_data["behavior"] == 'accelerate':
                                    cmd2car_que.put(3)
                                else:
                                    cmd2car_que.put(7)
                            elif req_data["direction"] == 'right':
                                if req_data["behavior"] == 'accelerate':
                                    cmd2car_que.put(4)
                                else:
                                    cmd2car_que.put(8)

                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to move!'
                            })
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'chmod':
                            if req_data["to"] == 'manual':
                                cmd2car_que.put(9)
                            elif req_data["to"] == 'auto-lane':
                                cmd2car_que.put(10)
                            elif req_data["to"] == 'auto-avoidance':
                                cmd2car_que.put(11)

                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to change my mode'
                            })
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'stop':
                            cmd2car_que.put(12)
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK to stop!'
                            })
                            conn.send(ret_d.encode('utf-8'))

                        elif req_prased["cmd"] == 'cam':
                            if req_data["direction"] == 'up':
                                if req_data["sign"] == 'start':
                                    cmd2car_que.put(14)
                                else:
                                    cmd2car_que.put(18)
                            elif req_data["direction"] == 'down':
                                if req_data["sign"] == 'start':
                                    cmd2car_que.put(15)
                                else:
                                    cmd2car_que.put(19)
                            elif req_data["direction"] == 'left':
                                if req_data["sign"] == 'start':
                                    cmd2car_que.put(16)
                                else:
                                    cmd2car_que.put(20)
                            elif req_data["direction"] == 'right':
                                if req_data["sign"] == 'start':
                                    cmd2car_que.put(17)
                                else:
                                    cmd2car_que.put(21)
                            ret_d = json.dumps({
                                "ret": 200,
                                "data": 'OK cam to move!'
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
    logger.remove()
    logger.add(sys.stdout,level='INFO')

    sensor2cmd_que=multiprocessing.Queue()
    cmd2car_que = multiprocessing.Queue()
    
    cmd_process = multiprocessing.Process(
        target=cmd_downstream, args=(cmd2car_que,sensor2cmd_que), daemon=True)
    cmd_process.start()
    
    sensor_process = multiprocessing.Process(
        target=env.env_core, args=(sensor2cmd_que,), daemon=True)
    sensor_process.start()

    car_process = multiprocessing.Process(
        target=car.car_main, args=(cmd2car_que,), daemon=True)
    car_process.start()
    
    # kill process
    cmd_process.join()
    car_process.join()
    def on_closing():
        cmd_process.terminate()
        car_process.terminate()
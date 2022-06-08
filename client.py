'''
Author       : Gehrychiang
LastEditTime : 2022-06-08 21:40:00
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
#客户端
import tkinter as tk
import socket
import cv2
import numpy as np
import time
import json
from PIL import Image, ImageTk
import multiprocessing
# config area
vid_port = 18081
cmd_port = 18082
localhost = '127.0.0.1'
remotehost = '192.168.1.101'
ip_addr = localhost
cmd_list = [
    '{"cmd":"ping","para":{}}',
    '{"cmd":"move","para":{"direction":"forward"}}',
    '{"cmd":"move","para":{"direction":"backward"}}',
    '{"cmd":"move","para":{"direction":"left"}}',
    '{"cmd":"move","para":{"direction":"right"}}',
    '{"cmd":"chmod","para":{"to":"manual"}}',
    '{"cmd":"chmod","para":{"to":"auto-lane"}}',
    '{"cmd":"chmod","para":{"to":"auto-avoidance"}}',
    '{"cmd":"stop","para":{}}',
    '{"cmd":"envStatus","para":{}}',
]
# config end

# global area
# que = queue.Queue()
# cmd_que = queue.Queue()
# sta_que = queue.Queue()
# global end


def vid_downstream(que, cmd_que, sta_que):
    while True:
        client = socket.socket()
        client.connect((ip_addr, vid_port))
        print('服务端已连接')
        while True:
            try:
                res = client.recv(65536)
                # print('已收到服务器信息：', res.decode('utf-8'))
                # res=client.recv(1024)
                # print(len(res))
                nparr = np.frombuffer(res, dtype='uint8')
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                img_tk = Image.fromarray(img)
                que.put(img_tk)
                # cv2.imshow('client_test',img)
                # key = cv2.waitKey(1) & 0xFF
                # if key == ord('q'):  # q键推出
                #     break
            except ConnectionResetError:
                print('连接断开，等待重新连接')
                client.close()
                break
            except Exception:
                print('连接终止，尝试重启')
                break


def cmd_upstream(que, cmd_que, sta_que):
    client = socket.socket()
    client.connect((ip_addr, cmd_port))
    print('服务端已连接')
    while True:
        try:
            # cmd is a json-like string
            # {"cmd":"move","para":{"direction":"forward"}}
            # {'cmd':'getStatus','para':{}}
            # {"ret": 200, "data": {}}
            while True:
                if not cmd_que.empty():
                    cmd = cmd_que.get()
                    if cmd==9:
                        tic1=time.perf_counter()
                        client.send(cmd_list[cmd].encode('utf-8'))
                        ret = client.recv(512).decode('utf-8')
                        tic2=time.perf_counter()
                        ret_d = json.loads(ret)
                        sta_que.put((ret_d["data"],(tic2-tic1)*1000))
                    else:
                        client.send(cmd_list[cmd].encode('utf-8'))
                        ret = client.recv(512).decode('utf-8')
                        ret_d = json.loads(ret)
                        print('响应结果 ', ret_d["data"])

                time.sleep(0.02)

        except ConnectionResetError:
            print('连接断开，等待重新连接')
            client.close()
            break
        except Exception:
            print('连接终止，尝试重启')
            time.sleep(10)
            client.close()
            break


def graphMain(que, cmd_que, sta_que):
    root = tk.Tk()
    root.title('RaspiCarSolution')
    # root.iconbitmap('favicon.ico')
    root.geometry('1280x720')
    root.resizable(False, False)
    root.configure(background='#F0F0F0')
    radiobut_val = tk.IntVar()
    radiobut_val.set(1)
    label = tk.Label(
        root,
        text='RaspiCarSolution',
        fg='#252526',
        bg='#F0F0F0',
        font=('Arial', 20))
    label.place(x=0, y=0, width=1280, height=50)
    vid_frame = tk.Label(root)
    vid_frame.place(x=213, y=55, width=854, height=480)

    # 四个方向键按钮
    def sendMoveCmd(event):
        cmd_que.put(event)
        radiobut_val.set(1)

    def sendChmodCmd(event):
        cmd_que.put(event)
        radiobut_val.set(event - 4)

    forward_but = tk.Button(
        root, text='↑', font=('Arial', 16),
        command=lambda: sendMoveCmd(1)).place(
            x=213 + 50, y=550, width=50, height=50)
    backward_but = tk.Button(
        root, text='↓', font=('Arial', 16),
        command=lambda: sendMoveCmd(2)).place(
            x=213 + 50, y=550 + 100, width=50, height=50)
    left_but = tk.Button(
        root, text='←', font=('Arial', 16),
        command=lambda: sendMoveCmd(3)).place(
            x=213, y=550 + 50, width=50, height=50)
    right_but = tk.Button(
        root, text='→', font=('Arial', 16),
        command=lambda: sendMoveCmd(4)).place(
            x=213 + 100, y=550 + 50, width=50, height=50)
    stop_but = tk.Button(
        root, text='X', font=('Arial', 16),
        command=lambda: sendMoveCmd(8)).place(
            x=213 + 50, y=550 + 50, width=50, height=50)

    # 按键捕获
    root.bind('<KeyPress-Up>', lambda event: sendMoveCmd(1))
    root.bind('<KeyPress-Down>', lambda event: sendMoveCmd(2))
    root.bind('<KeyPress-Left>', lambda event: sendMoveCmd(3))
    root.bind('<KeyPress-Right>', lambda event: sendMoveCmd(4))
    root.bind('<KeyPress-w>', lambda event: sendMoveCmd(1))
    root.bind('<KeyPress-d>', lambda event: sendMoveCmd(2))
    root.bind('<KeyPress-a>', lambda event: sendMoveCmd(3))
    root.bind('<KeyPress-s>', lambda event: sendMoveCmd(4))
    root.bind('<KeyPress-x>', lambda event: sendMoveCmd(8))
    root.bind('<KeyPress-1>', lambda event: sendChmodCmd(5))
    root.bind('<KeyPress-2>', lambda event: sendChmodCmd(6))
    root.bind('<KeyPress-3>', lambda event: sendChmodCmd(7))

    # 运行模式选择
    mode_label = tk.Label(
        root,
        text='Running Mode',
        fg='#252526',
        bg='#F0F0F0',
        font=('Arial', 15))
    mode_label.place(x=213 + 300, y=550 + 50, width=200, height=50)
    manual_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Manual',
        font=('Arial', 12),
        value=1,
        command=lambda: cmd_que.put(5))
    manual_but.place(x=213 + 500, y=550 + 50, width=100, height=50)
    auto1_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Auto-Lane',
        font=('Arial', 12),
        value=2,
        command=lambda: cmd_que.put(6))
    auto1_but.place(x=213 + 600, y=550 + 50, width=100, height=50)
    auto2_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Auto-Avoidance',
        font=('Arial', 12),
        value=3,
        command=lambda: cmd_que.put(7))
    auto2_but.place(x=213 + 700, y=550 + 50, width=150, height=50)

    # 温湿度模块
    temp_label = tk.Label(
        root,
        text='Temperature',
        fg='#252526',
        bg='#F0F0F0',
        font=('Arial', 15))
    temp_label.place(x=213 + 860, y=150, width=120, height=50)
    temp_val = tk.Label(
        root, text='null°', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    temp_val.place(x=213 + 980, y=150, width=90, height=50)
    humi_label = tk.Label(
        root, text='Humidity', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    humi_label.place(x=213 + 860, y=200, width=120, height=50)
    humi_val = tk.Label(
        root, text='null%', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    humi_val.place(x=213 + 980, y=200, width=90, height=50)

    rtt_label = tk.Label(
        root,
        text='ping',
        fg='#252526',
        bg='#F0F0F0',
        font=('Arial', 15)
    )
    rtt_label.place(x=10, y=100, width=40, height=50)
    rtt_val = tk.Label(
        root, text='460 ms', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    rtt_val.place(x=60, y=100, width=70, height=50)

    def sta_update():
        cmd_que.put(9)
        if not sta_que.empty():
            sta,ping = sta_que.get()
            sta = json.loads(sta)
            temp_val.config(text=str(sta["temp"]) + '°')
            humi_val.config(text=str(sta["humi"]) + '%')
            rtt_val.config(text=str(ping)[0:4] + 'ms')
        temp_val.after(2000, sta_update)
    
    def vid_update():
        # tic1=time.time()
        # print(que.qsize())
        if not que.empty():
            try:
                img = que.get()
                imgtk = ImageTk.PhotoImage(image=img)
                vid_frame.imgtk = imgtk
                vid_frame.configure(image=imgtk)
            except:
                pass
        # 5ms后重复以连续捕获
        # tic2=time.time()
        # print('need',tic2-tic1)
        vid_frame.after(5, vid_update)

    vid_update()
    sta_update()
    root.mainloop()


if __name__ == "__main__":
    que = multiprocessing.Queue()
    cmd_que = multiprocessing.Queue()
    sta_que = multiprocessing.Queue()

    graph_process = multiprocessing.Process(target=graphMain, args=(que, cmd_que, sta_que))
    graph_process.start()
    vid_process = multiprocessing.Process(target=vid_downstream, args=(que, cmd_que, sta_que))
    vid_process.start()
    cmd_process = multiprocessing.Process(target=cmd_upstream, args=(que, cmd_que, sta_que))
    cmd_process.start()
    
    def on_closing():
        graph_process.terminate()
        vid_process.terminate()
        cmd_process.terminate()
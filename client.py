'''
Author       : Gehrychiang
LastEditTime : 2022-06-20 17:10:07
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
#客户端
import tkinter as tk
import socket
import cv2
import time
import json
from PIL import Image, ImageTk
import multiprocessing
from loguru import logger
# import fire_recog

# config area
vid_port = 18081
cmd_port = 18082
localhost = '127.0.0.1'
remotehost = '192.168.1.102'
ip_addr = remotehost
cmd_list = [
    '{"cmd":"ping","para":"{}"}',  #0
    '{"cmd":"move","para":{"direction":"forward","behavior":"accelerate"}}',  #1
    '{"cmd":"move","para":{"direction":"backward","behavior":"accelerate"}}',  #2
    '{"cmd":"move","para":{"direction":"left","behavior":"accelerate"}}',  #3
    '{"cmd":"move","para":{"direction":"right","behavior":"accelerate"}}',  #4
    '{"cmd":"move","para":{"direction":"forward","behavior":"decelerate"}}',  #5
    '{"cmd":"move","para":{"direction":"backward","behavior":"decelerate"}}',  #6
    '{"cmd":"move","para":{"direction":"left","behavior":"decelerate"}}',  #7
    '{"cmd":"move","para":{"direction":"right","behavior":"decelerate"}}',  #8
    '{"cmd":"chmod","para":{"to":"manual"}}',  #9
    '{"cmd":"chmod","para":{"to":"auto-lane"}}',  #10
    '{"cmd":"chmod","para":{"to":"auto-avoidance"}}',  #11
    '{"cmd":"stop","para":{}}',  #12
    '{"cmd":"envStatus","para":{}}',  #13
    '{"cmd":"cam","para":{"direction":"up","sign":"start"}}',  #14
    '{"cmd":"cam","para":{"direction":"down","sign":"start"}}',  #15
    '{"cmd":"cam","para":{"direction":"left","sign":"start"}}',  #16
    '{"cmd":"cam","para":{"direction":"right","sign":"start"}}',  #17
    '{"cmd":"cam","para":{"direction":"up","sign":"stop"}}',  #18
    '{"cmd":"cam","para":{"direction":"down","sign":"stop"}}',  #19
    '{"cmd":"cam","para":{"direction":"left","sign":"stop"}}',  #20
    '{"cmd":"cam","para":{"direction":"right","sign":"stop"}}',  #21
]

# config end


def vid_downstream(que, cmd_que):
    while True:
        try:
            url = 'http://' + str(ip_addr) + ':' + str(vid_port) + '/stream'
            cap = cv2.VideoCapture(url)
            logger.info('<视频> 已连接到服务端')
            while True:
                try:
                    ret, frame = cap.read()
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    img_tk = Image.fromarray(img)
                    que.put(img_tk)
                    time.sleep(0.015) #用于匹配60fps
                except Exception:
                    logger.error('<视频> 连接终止，尝试重启')
                    break
        except Exception:
            logger.error('<视频> 服务器连接失败，3秒后尝试重启')
            time.sleep(1)
            logger.error('<视频> 服务器连接失败，2秒后尝试重启')
            time.sleep(1)
            logger.error('<视频> 服务器连接失败，1秒后尝试重启')
            time.sleep(1)
            while not cmd_que.empty():
                cmd_que.get()


def cmd_upstream(cmd_que, sta_que):
    while True:
        try:
            client = socket.socket()
            client.connect((ip_addr, cmd_port))
            logger.info('<指令> 已连接到服务端')
            while True:
                try:
                    # cmd 是一个json字符串，来自于cmd_list
                    while True:
                        if not cmd_que.empty():
                            cmd = cmd_que.get()
                            if cmd == 13:
                                tic1 = time.perf_counter()
                                client.send(cmd_list[cmd].encode('utf-8'))
                                ret = client.recv(512).decode('utf-8')
                                tic2 = time.perf_counter()
                                ret_d = json.loads(ret)
                                sta_que.put((ret_d["data"],
                                             (tic2 - tic1) * 1000))
                            else:
                                client.send(cmd_list[cmd].encode('utf-8'))
                                ret = client.recv(512).decode('utf-8')
                                ret_d = json.loads(ret)
                                logger.debug('收到服务器响应' + ' ' + str(ret_d))

                        time.sleep(0.02)

                except Exception:
                    logger.error('<指令> 连接终止，尝试重启')
                    client.close()
                    break
        except Exception:
            logger.error('<指令> 服务器连接失败，3秒后尝试重启')
            time.sleep(1)
            logger.error('<指令> 服务器连接失败，2秒后尝试重启')
            time.sleep(1)
            logger.error('<指令> 服务器连接失败，1秒后尝试重启')
            time.sleep(1)
            while not cmd_que.empty(): #清空cmd_que
                cmd_que.get()


def graphMain(que, cmd_que, sta_que):
    root = tk.Tk()
    #static area
    up_arrow_img = tk.PhotoImage(file='RaspiCarSolution\\static\\up_arrow.png')
    down_arrow_img = tk.PhotoImage(
        file='RaspiCarSolution\\static\\down_arrow.png')
    left_arrow_img = tk.PhotoImage(
        file='RaspiCarSolution\\static\\left_arrow.png')
    right_arrow_img = tk.PhotoImage(
        file='RaspiCarSolution\\static\\right_arrow.png')
    stop_img = tk.PhotoImage(file='RaspiCarSolution\\static\\stop.png')
    ping_img = tk.PhotoImage(file='RaspiCarSolution\\static\\ping.png')
    temperature_img = tk.PhotoImage(
        file='RaspiCarSolution\\static\\temperature.png')
    humidity_img = tk.PhotoImage(file='RaspiCarSolution\\static\\humidity.png')
    fire_bar_img = tk.PhotoImage(file='RaspiCarSolution\\static\\fire_bar.png')
    flame_img = tk.PhotoImage(file='RaspiCarSolution\\static\\flame.png')
    smile_img = tk.PhotoImage(file='RaspiCarSolution\\static\\smile.png')
    indicator_img = tk.PhotoImage(
        file='RaspiCarSolution\\static\\indicator.png')

    root.title('RaspiCarSolution')
    root.iconbitmap('RaspiCarSolution\\favicon.ico')
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
    vid_frame.place(x=320, y=55, width=640, height=480)

    # wsad按钮
    wsad_key_down = [False, False, False, False, False]

    def sendMoveCmd(event):
        if event >= 1 and event <= 4:
            if wsad_key_down[event] == False:
                cmd_que.put(event)
                wsad_key_down[event] = True
            else:
                pass
        elif event == 12:
            cmd_que.put(event)
        else:
            if wsad_key_down[event - 4] == False:
                cmd_que.put(event - 4)
                cmd_que.put(event)
            else:
                wsad_key_down[event - 4] = False
                cmd_que.put(event)
        radiobut_val.set(1)

    def sendChmodCmd(event):
        cmd_que.put(event)
        radiobut_val.set(event - 8)

    navi_key_down = [False, False, False, False, False]

    def sendCamCmd(event):
        if event >= 14 and event <= 17:
            if navi_key_down[event - 13] == False:
                cmd_que.put(event)
                navi_key_down[event - 13] = True
            else:
                pass
        else:
            if navi_key_down[event - 17] == False:
                cmd_que.put(event - 4)
                cmd_que.put(event)
            else:
                navi_key_down[event - 17] = False
                cmd_que.put(event)

    forward_but = tk.Button(
        root, image=up_arrow_img, command=lambda: sendMoveCmd(5))
    forward_but.place(x=213 + 50, y=550, width=50, height=50)

    backward_but = tk.Button(
        root, image=down_arrow_img, command=lambda: sendMoveCmd(6))
    backward_but.place(x=213 + 50, y=550 + 100, width=50, height=50)
    left_but = tk.Button(
        root, image=left_arrow_img, command=lambda: sendMoveCmd(7))
    left_but.place(x=213, y=550 + 50, width=50, height=50)
    right_but = tk.Button(
        root, image=right_arrow_img, command=lambda: sendMoveCmd(8))
    right_but.place(x=213 + 100, y=550 + 50, width=50, height=50)
    stop_but = tk.Button(root, image=stop_img, command=lambda: sendMoveCmd(12))
    stop_but.place(x=213 + 50, y=550 + 50, width=50, height=50)

    # 按键捕获
    root.bind('<KeyPress-Up>', lambda event: sendCamCmd(14))
    root.bind('<KeyPress-Down>', lambda event: sendCamCmd(15))
    root.bind('<KeyPress-Left>', lambda event: sendCamCmd(16))
    root.bind('<KeyPress-Right>', lambda event: sendCamCmd(17))
    root.bind('<KeyRelease-Up>', lambda event: sendCamCmd(18))
    root.bind('<KeyRelease-Down>', lambda event: sendCamCmd(19))
    root.bind('<KeyRelease-Left>', lambda event: sendCamCmd(20))
    root.bind('<KeyRelease-Right>', lambda event: sendCamCmd(21))

    root.bind('<KeyPress-w>', lambda event: sendMoveCmd(1))
    root.bind('<KeyPress-s>', lambda event: sendMoveCmd(2))
    root.bind('<KeyPress-a>', lambda event: sendMoveCmd(3))
    root.bind('<KeyPress-d>', lambda event: sendMoveCmd(4))
    root.bind('<KeyRelease-w>', lambda event: sendMoveCmd(5))
    root.bind('<KeyRelease-s>', lambda event: sendMoveCmd(6))
    root.bind('<KeyRelease-a>', lambda event: sendMoveCmd(7))
    root.bind('<KeyRelease-d>', lambda event: sendMoveCmd(8))

    root.bind('<KeyPress-x>', lambda event: sendMoveCmd(12))
    root.bind('<KeyPress-1>', lambda event: sendChmodCmd(9))
    root.bind('<KeyPress-2>', lambda event: sendChmodCmd(10))
    root.bind('<KeyPress-3>', lambda event: sendChmodCmd(11))

    # 运行模式选择
    mode_label = tk.Label(
        root,
        text='Running Mode',
        fg='#252526',
        bg='#F0F0F0',
        font=('Arial', 17))
    mode_label.place(x=213 + 250, y=550 + 50, width=200, height=50)
    manual_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Manual',
        font=('Arial', 15),
        value=1,
        command=lambda: cmd_que.put(9))
    manual_but.place(x=213 + 450, y=550 + 50, width=90, height=50)
    auto1_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Auto-Lane',
        font=('Arial', 15),
        value=2,
        command=lambda: cmd_que.put(10))
    auto1_but.place(x=213 + 550, y=550 + 50, width=120, height=50)
    auto2_but = tk.Radiobutton(
        root,
        variable=radiobut_val,
        text='Auto-Avoidance',
        font=('Arial', 15),
        value=3,
        command=lambda: cmd_que.put(11))
    auto2_but.place(x=213 + 675, y=550 + 50, width=170, height=50)

    # 温湿度模块
    temp_label = tk.Label(root, image=temperature_img)
    temp_label.place(x=213 + 880, y=150, width=100, height=50)
    temp_val = tk.Label(
        root, text='null°C', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    temp_val.place(x=213 + 950, y=150, width=90, height=50)
    humi_label = tk.Label(root, image=humidity_img)
    humi_label.place(x=213 + 880, y=200, width=100, height=50)
    humi_val = tk.Label(
        root, text='null%', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    humi_val.place(x=213 + 950, y=200, width=90, height=50)

    rtt_label = tk.Label(
        root, image=ping_img, fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    rtt_label.place(x=10, y=100, width=40, height=50)
    rtt_val = tk.Label(
        root, text='460 ms', fg='#252526', bg='#F0F0F0', font=('Arial', 15))
    rtt_val.place(x=60, y=100, width=70, height=50)

    # 火情显示(百分比条)
    fire_label = tk.Label(root, image=fire_bar_img)
    fire_label.place(x=1010 + 10, y=300, width=225, height=20)
    smile_label = tk.Label(root, image=smile_img)
    smile_label.place(x=1010 - 15 + 10, y=260, width=40, height=40)
    flame_label = tk.Label(root, image=flame_img)
    flame_label.place(x=1010 + 205 + 10, y=260, width=40, height=40)
    fire_val = tk.Label(root, image=indicator_img)
    fire_val.place(x=1007 + 110, y=320, width=30, height=30)

    def sta_send():
        cmd_que.put(13)
        root.after(2000, sta_send)

    def sta_update():
        if not sta_que.empty():
            sta, ping = sta_que.get()
            sta = json.loads(sta)
            temp_val.config(text=str(sta["temp"]) + '°C')
            humi_val.config(text=str(sta["humi"]) + '%')
            rtt_val.config(text=str(ping)[0:4] + 'ms')
            fire_val.place(
                x=1007 + sta["fire"] * 220, y=320, width=30, height=30)
        root.after(100, sta_update)

    def vid_update():
        # print(que.qsize())
        if not que.empty():
            try:
                img = que.get()
                imgtk = ImageTk.PhotoImage(image=img)
                vid_frame.imgtk = imgtk
                vid_frame.configure(image=imgtk)
            except:
                pass
        vid_frame.after(5, vid_update)

    sta_send()
    vid_update()
    sta_update()
    root.mainloop()


if __name__ == "__main__":
    vid_que = multiprocessing.Queue()
    cmd_que = multiprocessing.Queue()
    sta_que = multiprocessing.Queue()

    graph_process = multiprocessing.Process(
        target=graphMain, args=(vid_que, cmd_que, sta_que))
    graph_process.start()

    vid_process = multiprocessing.Process(
        target=vid_downstream, args=(vid_que, cmd_que))
    vid_process.start()

    cmd_process = multiprocessing.Process(
        target=cmd_upstream, args=(cmd_que, sta_que))
    cmd_process.start()

    def on_closing():
        graph_process.terminate()
        vid_process.terminate()
        cmd_process.terminate()
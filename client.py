'''
Author       : Gehrychiang
LastEditTime : 2022-06-07 12:49:55
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
#客户端
import tkinter as tk
import tkinter.ttk as ttk
import queue
import socket
import threading
from turtle import back, color
import cv2
import numpy as np
import time
import json
from PIL import Image, ImageTk
# config area
vid_port=18081
cmd_port=18082
localhost='127.0.0.1'
ip_addr=localhost
# config end

# global area
que=queue.Queue()
cmd_que=queue.Queue()
# global end

def vid_downstream():
    while True:
        client = socket.socket()
        client.connect((ip_addr, vid_port))
        print('服务端已连接')
        while True:
            try:
                res=client.recv(262144)
                # print('已收到服务器信息：', res.decode('utf-8'))
                # res=client.recv(1024)
                # print('received',len(res))
                nparr = np.frombuffer(res, dtype='uint8')
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                img_tk = img
                que.put(img_tk)
                # cv2.imshow('client_test',im)
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

def cmd_upstream():
    # while True:
    #     if cmd_que.empty()==False:
    #         cmd=cmd_que.get()
    #         print('收到命令：', cmd)
    #     time.sleep(0.1)
    client = socket.socket()
    client.connect((ip_addr, cmd_port))
    print('服务端已连接')
    while True:
        try:
            # cmd is a json-like string
            # {'cmd':'move','para':{'direction':'forward','speed':'0.5'}}
            # {'cmd':'getStatus','para':{}}
            # {"ret": 200, "data": {}}
            while True:
                if not cmd_que.empty():
                    cmd=cmd_que.get()
                    cmd_d=json.dumps({"cmd":cmd,"para":{}})
                    client.send(cmd_d.encode('utf-8'))
                time.sleep(0.1)

            # cmd_exp='{"cmd":"getStatus","para":{}}'
            # client.send(cmd_exp.encode('utf-8'))
            # ret=client.recv(512).decode('utf-8')
            # ret_d=json.loads(ret)
            # print('响应结果 ',ret_d["data"]["status"])

        except ConnectionResetError:
            print('连接断开，等待重新连接')
            client.close()
            break
        except Exception:
            print('连接终止，尝试重启')
            time.sleep(10)
            client.close()
            break

def graphMain():
    root = tk.Tk()
    root.title('RaspiCarSolution')
    root.geometry('1280x720')
    root.resizable(False, False)
    root.configure(background='#F0F0F0')
    label = tk.Label(root, text='RaspiCarSolution',fg='#252526', bg='#F0F0F0', font=('Arial', 20))
    label.place(x=0, y=0, width=1280, height=50)
    vid_frame = tk.Label(root)
    vid_frame.place(x=213, y=55, width=854, height=480)
    def vid_update():
        if not que.empty():
            cv2image= que.get()
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = img)
            vid_frame.imgtk = imgtk
            vid_frame.configure(image=imgtk)
            # 15ms后重复以连续捕获
        vid_frame.after(10, vid_update)
    
    # 四个方向键按钮
    forward_but=tk.Button(root, text='↑',font=('Arial', 16), command=lambda: cmd_que.put(1)).place(x=213+50, y=550, width=50, height=50)
    backward_but=tk.Button(root, text='↓',font=('Arial', 16), command=lambda: cmd_que.put(2)).place(x=213+50, y=550+100, width=50, height=50)
    left_but=tk.Button(root, text='←',font=('Arial', 16), command=lambda: cmd_que.put(3)).place(x=213, y=550+50, width=50, height=50)
    right_but=tk.Button(root, text='→',font=('Arial', 16), command=lambda: cmd_que.put(4)).place(x=213+100, y=550+50, width=50, height=50)
    # 方向键捕获
    root.bind('<KeyPress-Up>', lambda event: cmd_que.put(1))
    root.bind('<KeyPress-Down>', lambda event: cmd_que.put(2))
    root.bind('<KeyPress-Left>', lambda event: cmd_que.put(3))
    root.bind('<KeyPress-Right>', lambda event: cmd_que.put(4))
    root.bind('<KeyPress-w>', lambda event: cmd_que.put(1))
    root.bind('<KeyPress-d>', lambda event: cmd_que.put(2))
    root.bind('<KeyPress-a>', lambda event: cmd_que.put(3))
    root.bind('<KeyPress-s>', lambda event: cmd_que.put(4))
    # 运行模式选择
    mode_label=tk.Label(root, text='Running Mode',fg='#252526', bg='#F0F0F0', font=('Arial', 12))
    mode_label.place(x=213+300, y=550+50, width=200, height=50)
    manual_but=tk.Radiobutton(root, text='Manual',font=('Arial', 12),  value=1, command=lambda: cmd_que.put(5)).place(x=213+500, y=550+50, width=100, height=50)
    auto1_but=tk.Radiobutton(root, text='Auto-Lane',font=('Arial', 12),  value=2, command=lambda: cmd_que.put(6)).place(x=213+600, y=550+50, width=100, height=50)
    auto2_but=tk.Radiobutton(root, text='Auto-Avoidance',font=('Arial', 12),  value=3, command=lambda: cmd_que.put(7)).place(x=213+700, y=550+50, width=150, height=50)
    
    vid_update()
    
    root.mainloop()

if __name__ == "__main__":
    graph_thread=threading.Thread(target=graphMain)
    graph_thread.start()
    vid_thread = threading.Thread(target=vid_downstream)
    vid_thread.start()
    cmd_thread=threading.Thread(target=cmd_upstream)
    cmd_thread.start()
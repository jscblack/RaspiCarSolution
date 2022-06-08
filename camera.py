'''
Author       : Gehrychiang
LastEditTime : 2022-06-08 19:42:48
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
# used for capture  the video from the camera
# store into shared_memory
# 这一进程将持续获取摄像头的视频流，并将其存储到共享内存中

import cv2
from multiprocessing import  shared_memory
import numpy as np

def camera_capture(arr_name):
    shm_ghost=shared_memory.SharedMemory(name=arr_name)
    arr=np.ndarray(shape=(480,854,3),dtype=np.uint8,buffer=shm_ghost.buf)
    
    cap = cv2.VideoCapture(0)
    # configs
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # width=1920
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # height=1080
    cap.set(cv2.CAP_PROP_FPS, 60) # fps=60
    # time.sleep(2) # wait for initilize
    if not cap.isOpened():
        print('open camrea failed')
        exit(0)
    else:
        print('camrea start runnning...')
        while True:
            ret, frame = cap.read()
            frame=cv2.resize(frame,dsize=[854, 480])
            # len = 1229760=854*480*3*1 byte
            arr[:]=frame[:]
            # push it to shared_memory
            
            # cv2.imshow("a", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):  #等待按键q按下
            #     break

# def camera_show(arr_name):
#     shm_ghost=shared_memory.SharedMemory(name=arr_name)
#     arr=np.ndarray(shape=(480,854,3),dtype=np.uint8,buffer=shm_ghost.buf)
#     while True:
#         cv2.imshow("b", arr)
#         if cv2.waitKey(1) & 0xFF == ord('q'):  #等待按键q按下
#             break

# if __name__ == "__main__":
    # cam_lock=multiprocessing.Lock()
    # cam_shm=shared_memory.SharedMemory(create=True,size=854*480*3)
    # print(cam_shm.name)
    # cam_main=multiprocessing.Process(target=camera_capture,args=(cam_shm.name,), daemon=True)
    # cam_sub=multiprocessing.Process(target=camera_show,args=(cam_shm.name,),daemon=True)
    # cam_main.start()
    # time.sleep(2)
    # cam_sub.start()
    # cam_sub.join()
    # cam_main.join()
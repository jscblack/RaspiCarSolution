'''
Author       : Gehrychiang
LastEditTime : 2022-06-06 15:21:56
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import threading

# def_main_thread_func
def main_thread_func():
    # TODO
    for iter in range(10):
        print("main thread is running")
def sec_thread_func():
    # TODO
    for iter in range(10):
        print("sec thread is running")
def thd_thread_func():
    # TODO
    for iter in range(10):
        print("thd thread is running")

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_thread_func)
    sec_thread = threading.Thread(target=sec_thread_func)
    thd_thread = threading.Thread(target=thd_thread_func)
    main_thread.start()
    sec_thread.start()
    thd_thread.start()
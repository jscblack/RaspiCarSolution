'''
Author       : Gehrychiang
LastEditTime : 2022-06-12 13:27:03
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''

from multiprocessing import shared_memory
import numpy as np

# predict_fire is the only func you exposed to me
# you will need some extra funcs for yourself
def predict_fire(arr_name,fire_que):
    shm_ghost = shared_memory.SharedMemory(name=arr_name)
    img = np.ndarray(shape=(480, 854, 3), dtype=np.uint8, buffer=shm_ghost.buf)
    # TODO:
    # this is your img
    # you need to return a true or false back to me
    # just like below
    # fire_que.put([True,img_res])
    # fire_que.put([False,img_res])

if __name__ == "__main__":
    onnx_model_path = 'RaspiCarSolution\\fire-flame.onnx'
    sess = rt.InferenceSession(onnx_model_path)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    print(input_name, label_name)
    pass

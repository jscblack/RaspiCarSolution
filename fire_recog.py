'''
Author       : Gehrychiang
LastEditTime : 2022-06-14 17:29:55
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import numpy as np
import cv2
from loguru import logger
import time
import tflite_runtime.interpreter as tflite

# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="fire_lite_opt.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# print(input_details)
# print(output_details)


while True:
    cap=cv2.VideoCapture('http://192.168.1.102:18081/stream')
    _,img=cap.read()
    img=cv2.resize(img,dsize=(224,224))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    input_data = np.asarray(img, dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0) /255
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Predict
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(output_data)
    cap.release()
    time.sleep(2)

if __name__ == "__main__":
    pass

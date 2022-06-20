'''
Author       : Gehrychiang
LastEditTime : 2022-06-20 17:10:18
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import numpy as np
import cv2
from loguru import logger
import tflite_runtime.interpreter as tflite

def predict_fire(url):
    logger.debug('<TFlite> 开始计算前向网络')
    # Load the TFLite model and allocate tensors.
    interpreter = tflite.Interpreter(model_path='/home/pi/proj/RaspiCarSolution/fire_lite.tflite')
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # print(input_details)
    # print(output_details)

    cap=cv2.VideoCapture(url)
    _,img=cap.read()
    img=cv2.resize(img,dsize=(224,224))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    input_data = np.asarray(img, dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0) /255
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # Predict
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    cap.release()
    logger.info('<TFlite> 前向网络推理完成')
    return (1,float(output_data[0][0]))

if __name__ == "__main__":
    pass


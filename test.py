'''
Author       : Gehrychiang
LastEditTime : 2022-06-16 15:51:54
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
from loguru import logger
import RPi.GPIO as GPIO
import threading
import time
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

def servo_appointed_detection(pos):
    pwm_FrontServo.ChangeDutyCycle(2.5 + 10 * pos / 180)
    time.sleep(0.3)
    pwm_FrontServo.ChangeDutyCycle(0)

IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13
FrontServoPin = 23

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)
#忽略警告信息
GPIO.setwarnings(False)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(FrontServoPin, GPIO.OUT)

pwm_ENA = GPIO.PWM(ENA, 2000)
pwm_ENB = GPIO.PWM(ENB, 2000)
pwm_ENA.start(0)
pwm_ENB.start(0)
pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
pwm_FrontServo.start(0)

servo_appointed_detection(-5)
time.sleep(0.5)
servo_appointed_detection(88)
time.sleep(0.5)
servo_appointed_detection(190)
time.sleep(0.5)
servo_appointed_detection(88)
time.sleep(0.5)
pwm_ENA.stop()
pwm_ENB.stop()
pwm_FrontServo.stop()
GPIO.cleanup()





# import numpy as np
# import cv2
# from loguru import logger
# import time
# import tflite_runtime.interpreter as tflite

# def predict_fire(url):
#     logger.info('<TFlite> 开始计算前向网络')
#     # Load the TFLite model and allocate tensors.
#     interpreter = tflite.Interpreter(model_path="fire_lite_opt.tflite")
#     interpreter.allocate_tensors()

#     # Get input and output tensors.
#     input_details = interpreter.get_input_details()
#     output_details = interpreter.get_output_details()

#     # print(input_details)
#     # print(output_details)

#     cap=cv2.VideoCapture(url)
#     _,img=cap.read()
#     img=cv2.resize(img,dsize=(224,224))
#     img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#     input_data = np.asarray(img, dtype=np.float32)
#     input_data = np.expand_dims(input_data, axis=0) /255
#     interpreter.set_tensor(input_details[0]['index'], input_data)
#     # Predict
#     interpreter.invoke()
#     output_data = interpreter.get_tensor(output_details[0]['index'])
#     print(output_data)
#     cap.release()
#     return (1,output_data[0][0])

# if __name__ == "__main__":
#     predict_fire('http://127.0.0.1:18081/snapshot')


# import RPi.GPIO as GPIO
# import time
# #舵机引脚定义
# FrontServoPin = 23
# ServoUpDownPin = 9
# ServoLeftRightPin = 11
# #设置GPIO口为BCM编码方式
# GPIO.setmode(GPIO.BCM)
# #忽略警告信息
# GPIO.setwarnings(False)
# GPIO.setup(FrontServoPin, GPIO.OUT)
# GPIO.setup(ServoUpDownPin, GPIO.OUT)
# GPIO.setup(ServoLeftRightPin, GPIO.OUT)
# pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
# pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
# pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
# pwm_FrontServo.start(0)
# pwm_UpDownServo.start(0)
# pwm_LeftRightServo.start(0)
# print('ok')
# angle=50
# pwm_UpDownServo.ChangeDutyCycle(2.5 + (angle+90)*10/180)
# # pwm_LeftRightServo.ChangeDutyCycle(100)
# time.sleep(0.02)
# pwm_UpDownServo.ChangeDutyCycle(0)
# time.sleep(2)
# pwm_UpDownServo.ChangeDutyCycle(2.5 + (-angle+90)*10/180)
# time.sleep(0.02)
# pwm_UpDownServo.ChangeDutyCycle(0)

# pwm_FrontServo.stop()
# pwm_LeftRightServo.stop()
# pwm_UpDownServo.stop()
# GPIO.cleanup()
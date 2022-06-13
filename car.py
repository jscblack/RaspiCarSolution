'''
Author       : Gehrychiang
LastEditTime : 2022-06-13 09:11:04
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
from loguru import logger
# import RPi.GPIO as GPIO
import threading
import time


def car_main(cmd_que):

    #按键值定义
    run_car = '1'  #按键前
    back_car = '2'  #按键后
    left_car = '3'  #按键左
    right_car = '4'  #按键右
    stop_car = '0'  #按键停

    #舵机按键值定义
    front_left_servo = '1'  #前舵机向左
    front_right_servo = '2'  #前舵机向右
    up_servo = '3'  #摄像头舵机向上
    down_servo = '4'  #摄像头舵机向下
    left_servo = '6'  #摄像头舵机向左
    right_servo = '7'  #摄像头舵机向右
    updowninit_servo = '5'  #摄像头舵机上下复位
    stop_servo = '8'  #舵机停止

    #小车状态值定义
    enSTOP = 0
    enRUN = 1
    enBACK = 2
    enLEFT = 3
    enRIGHT = 4
    enTLEFT = 5
    enTRIGHT = 6

    #小车舵机定义
    enFRONTSERVOLEFT = 1
    enFRONTSERVORIGHT = 2
    enSERVOUP = 3
    enSERVODOWN = 4
    enSERVOUPDOWNINIT = 5
    enSERVOLEFT = 6
    enSERVORIGHT = 7
    enSERVOSTOP = 8

    #初始化上下左右角度为90度
    ServoLeftRightPos = 90
    ServoUpDownPos = 90
    g_frontServoPos = 90
    g_nowfrontPos = 0

    #小车电机引脚定义
    IN1 = 20
    IN2 = 21
    IN3 = 19
    IN4 = 26
    ENA = 16
    ENB = 13

    #小车按键定义
    key = 8

    #超声波引脚定义
    EchoPin = 0
    TrigPin = 1

    #RGB三色灯引脚定义
    LED_R = 22
    LED_G = 27
    LED_B = 24

    #舵机引脚定义
    FrontServoPin = 23
    ServoUpDownPin = 9
    ServoLeftRightPin = 11

    #红外避障引脚定义
    AvoidSensorLeft = 12
    AvoidSensorRight = 17

    #蜂鸣器引脚定义
    buzzer = 8

    #灭火电机引脚设置
    OutfirePin = 2

    #循迹红外引脚定义
    #TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
    #      3                 5                  4                   18
    TrackSensorLeftPin1 = 3  #定义左边第一个循迹红外传感器引脚为3口
    TrackSensorLeftPin2 = 5  #定义左边第二个循迹红外传感器引脚为5口
    TrackSensorRightPin1 = 4  #定义右边第一个循迹红外传感器引脚为4口
    TrackSensorRightPin2 = 18  #定义右边第二个循迹红外传感器引脚为18口

    #光敏电阻引脚定义
    LdrSensorLeft = 7
    LdrSensorRight = 6

    #变量的定义
    #七彩灯RGB三色变量定义
    red = 0
    green = 0
    blue = 0
    #小车和舵机状态变量
    g_CarState = 0
    g_ServoState = 0
    #小车速度变量
    Gradient=5
    aheading=True
    CarSpeedLeft = 0
    CarSpeedRight = 0
    #寻迹，避障，寻光变量
    infrared_track_value = ''
    infrared_avoid_value = ''
    LDR_value = ''
    g_lednum = 0

    #电机引脚初始化为输出模式
    #按键引脚初始化为输入模式
    #超声波,RGB三色灯,舵机引脚初始化
    #红外避障引脚初始化
    def init():
        #设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)
        #忽略警告信息
        GPIO.setwarnings(False)

        global pwm_ENA
        global pwm_ENB
        global pwm_FrontServo
        global pwm_UpDownServo
        global pwm_LeftRightServo
        global pwm_rled
        global pwm_gled
        global pwm_bled
        GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(OutfirePin, GPIO.OUT)
        GPIO.setup(EchoPin, GPIO.IN)
        GPIO.setup(TrigPin, GPIO.OUT)
        GPIO.setup(LED_R, GPIO.OUT)
        GPIO.setup(LED_G, GPIO.OUT)
        GPIO.setup(LED_B, GPIO.OUT)
        GPIO.setup(FrontServoPin, GPIO.OUT)
        GPIO.setup(ServoUpDownPin, GPIO.OUT)
        GPIO.setup(ServoLeftRightPin, GPIO.OUT)
        GPIO.setup(AvoidSensorLeft, GPIO.IN)
        GPIO.setup(AvoidSensorRight, GPIO.IN)
        GPIO.setup(LdrSensorLeft, GPIO.IN)
        GPIO.setup(LdrSensorRight, GPIO.IN)
        GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
        GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
        GPIO.setup(TrackSensorRightPin1, GPIO.IN)
        GPIO.setup(TrackSensorRightPin2, GPIO.IN)
        #设置pwm引脚和频率为2000hz
        pwm_ENA = GPIO.PWM(ENA, 2000)
        pwm_ENB = GPIO.PWM(ENB, 2000)
        pwm_ENA.start(0)
        pwm_ENB.start(0)
        #设置舵机的频率和起始占空比
        pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
        pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
        pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
        pwm_FrontServo.start(0)
        pwm_UpDownServo.start(0)
        pwm_LeftRightServo.start(0)
        pwm_rled = GPIO.PWM(LED_R, 1000)
        pwm_gled = GPIO.PWM(LED_G, 1000)
        pwm_bled = GPIO.PWM(LED_B, 1000)
        pwm_rled.start(0)
        pwm_gled.start(0)
        pwm_bled.start(0)
        logger.debug('车辆动作机构初始化完成')

    #小车前进
    def run():
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
        pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))

    #小车后退
    def back():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
        pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))

    #小车左转
    def left():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
        pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))

    #小车右转
    def right():
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
        pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))

    # #小车原地左转
    # def spin_left():
    #     GPIO.output(IN1, GPIO.LOW)
    #     GPIO.output(IN2, GPIO.HIGH)
    #     GPIO.output(IN3, GPIO.HIGH)
    #     GPIO.output(IN4, GPIO.LOW)
    #     pwm_ENA.ChangeDutyCycle(abs(CarSpeedControl))
    #     pwm_ENB.ChangeDutyCycle(abs(CarSpeedControl))

    # #小车原地右转
    # def spin_right():
    #     GPIO.output(IN1, GPIO.HIGH)
    #     GPIO.output(IN2, GPIO.LOW)
    #     GPIO.output(IN3, GPIO.LOW)
    #     GPIO.output(IN4, GPIO.HIGH)
    #     pwm_ENA.ChangeDutyCycle(abs(CarSpeedControl))
    #     pwm_ENB.ChangeDutyCycle(abs(CarSpeedControl))

    #小车停止
    def brake():
        CarSpeedLeft = 0
        CarSpeedRight = 0
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

    #关闭GPIO口
    def shutdown():
        pwm_ENA.stop()
        pwm_ENB.stop()
        pwm_rled.stop()
        pwm_gled.stop()
        pwm_bled.stop()
        pwm_FrontServo.stop()
        pwm_LeftRightServo.stop()
        pwm_UpDownServo.stop()
        GPIO.cleanup()
        logger.debug('车辆动作机构解构完成')
    status = {
        'forward': False,
        'backward': False,
        'left': False,
        'right': False
    }
    maxSpeed = 50

    def motor_ctl_thread(status):
        # CarSpeedLeft = 0
        # CarSpeedRight = 0
        
        while True:
            # 只允许与行进方向相同时的加速行进+转向
            # 不允许向前行进时backward转向
            # 不允许向后行进时forward转向
            if not status['forward'] and not status['backward'] and not status['left'] and not status['right']:
                #0000
                if aheading:
                    if CarSpeedLeft != CarSpeedRight:
                        CarSpeedLeft = min(CarSpeedLeft, CarSpeedRight)
                        CarSpeedRight = min(CarSpeedLeft, CarSpeedRight)
                    else:
                        CarSpeedLeft=max(CarSpeedLeft-Gradient, 0)
                        CarSpeedRight=max(CarSpeedRight-Gradient, 0)
                        if(CarSpeedLeft==0 and CarSpeedRight==0):
                            aheading=False
                else:
                    if CarSpeedLeft != CarSpeedRight:
                        CarSpeedLeft = max(CarSpeedLeft, CarSpeedRight)
                        CarSpeedRight = max(CarSpeedLeft, CarSpeedRight)
                    else:
                        CarSpeedLeft=min(CarSpeedLeft+Gradient, 0)
                        CarSpeedRight=min(CarSpeedRight+Gradient, 0)
                        if(CarSpeedLeft==0 and CarSpeedRight==0):
                            aheading=True
            elif status['forward'] and not status['backward'] and not status['left'] and not status['right']:
                #1000
                if aheading:
                    CarSpeedLeft = min(CarSpeedLeft+Gradient, maxSpeed)
                    CarSpeedRight = min(CarSpeedRight+Gradient, maxSpeed)
                else:
                    CarSpeedLeft = min(CarSpeedLeft+2*Gradient, 0)
                    CarSpeedRight = min(CarSpeedRight+2*Gradient, 0)
                    if(CarSpeedLeft==0 and CarSpeedRight==0):
                        aheading=True
            elif not status['forward'] and status['backward'] and not status['left'] and not status['right']:
                #0100
                # need further implementation
                if aheading:
                    CarSpeedLeft=max(CarSpeedLeft-2*Gradient, 0)
                    CarSpeedRight=max(CarSpeedRight-2*Gradient, 0)
                    if(CarSpeedLeft==0 and CarSpeedRight==0):
                        aheading=False
                else:
                    CarSpeedLeft = max(CarSpeedLeft-Gradient, -maxSpeed)
                    CarSpeedRight = max(CarSpeedRight-Gradient, -maxSpeed)
                        
            elif not status['forward'] and not status['backward'] and status['left'] and not status['right']:
                #0010
                pass
            elif not status['forward'] and not status['backward'] and not status['left'] and status['right']:
                #0001
                pass
            elif status['forward'] and status['backward'] and not status['left'] and not status['right']:
                #1100
                pass
            elif status['forward'] and not status['backward'] and status['left'] and not status['right']:
                #1010
                pass
            elif status['forward'] and not status['backward'] and not status['left'] and status['right']:
                #1001
                pass
            elif not status['forward'] and status['backward'] and status['left'] and not status['right']:
                #0110
                pass
            elif not status['forward'] and status['backward'] and not status['left'] and status['right']:
                #0101
                pass
            elif status['forward'] and status['backward'] and status['left'] and not status['right']:
                #1110
                pass
            elif status['forward'] and status['backward'] and not status['left'] and status['right']:
                #1101
                pass
            elif not status['forward'] and not status['backward'] and status['left'] and status['right']:
                #0011
                pass
            elif not status['forward'] and not status['backward'] and status['left'] and status['right']:
                #0011
                pass
            elif status['forward'] and status['backward'] and status['left'] and status['right']:
                #1111
                pass
            
            if CarSpeedLeft > 0:
                GPIO.output(IN1, GPIO.HIGH)
                GPIO.output(IN3, GPIO.LOW)
                pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
            else:
                GPIO.output(IN1, GPIO.LOW)
                GPIO.output(IN3, GPIO.HIGH)
                pwm_ENA.ChangeDutyCycle(abs(CarSpeedLeft))
            if CarSpeedRight > 0:
                GPIO.output(IN2, GPIO.HIGH)
                GPIO.output(IN4, GPIO.LOW)
                pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))
            else:
                GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN4, GPIO.HIGH)
                pwm_ENB.ChangeDutyCycle(abs(CarSpeedRight))

            time.sleep(1)

    # init()

    running_mode = 1
    # mode 1 2 3
    # 1: manual
    # 2: auto-lane
    # 3: auto-avoid

    cnt = 100
    motor_ctl_thread = threading.Thread(
        target=motor_ctl_thread, args=(status, ))
    motor_ctl_thread.start()
    while True:
        if not cmd_que.empty():
            cmd = cmd_que.get()
            # cnt = cnt - 1
            # if cnt == 0:
            #     shutdown()
            #     logger.debug('次数用尽运行结束')
            #     break

            if cmd == 1:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['forward'] = True
                logger.debug('车辆给油')
            elif cmd == 2:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['backward'] = True
                logger.debug('车辆刹车')
            elif cmd == 3:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['left'] = True
                logger.debug('车辆左转')
            elif cmd == 4:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['right'] = True
                logger.debug('车辆右转')

            elif cmd == 5:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['forward'] = False
                logger.debug('车辆停止给油')

            elif cmd == 6:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['backward'] = False
                logger.debug('车辆停止给油')

            elif cmd == 7:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['left'] = False
                logger.debug('车辆停止给油')

            elif cmd == 8:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                status['right'] = False
                logger.debug('车辆停止给油')

            elif cmd == 9:
                running_mode = 1
                # set gpio here
                logger.warning('车辆动作机构已切换到手动模式')
            elif cmd == 10:
                running_mode = 2
                # set gpio here
                logger.warning('车辆动作机构已切换到自动车道模式')
            elif cmd == 11:
                running_mode = 3
                # set gpio here
                logger.warning('车辆动作机构已切换到自动避障模式')
            elif cmd == 12:
                if running_mode != 1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                brake()
                shutdown()
                logger.debug('车辆停止')
        time.sleep(0.1)


if __name__ == "__main__":
    pass
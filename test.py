import RPi.GPIO as GPIO
import time
#舵机引脚定义
FrontServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11
#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)
#忽略警告信息
GPIO.setwarnings(False)
GPIO.setup(FrontServoPin, GPIO.OUT)
GPIO.setup(ServoUpDownPin, GPIO.OUT)
GPIO.setup(ServoLeftRightPin, GPIO.OUT)
pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
pwm_FrontServo.start(0)
pwm_UpDownServo.start(0)
pwm_LeftRightServo.start(0)
print('ok')
angle=50
pwm_UpDownServo.ChangeDutyCycle(2.5 + (angle+90)*10/180)
# pwm_LeftRightServo.ChangeDutyCycle(100)
time.sleep(0.02)
pwm_UpDownServo.ChangeDutyCycle(0)
time.sleep(2)
pwm_UpDownServo.ChangeDutyCycle(2.5 + (-angle+90)*10/180)
time.sleep(0.02)
pwm_UpDownServo.ChangeDutyCycle(0)

pwm_FrontServo.stop()
pwm_LeftRightServo.stop()
pwm_UpDownServo.stop()
GPIO.cleanup()
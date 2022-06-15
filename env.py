'''
Author       : Gehrychiang
LastEditTime : 2022-06-15 20:36:37
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import fire_recog
import cv2
import sensor_base
import numpy as np
from loguru import logger
import time

logger.add(level='INFO') # 设置只输出info以上的日志
localhost = '127.0.0.1'
vid_port=18081
def env_core(sensor2cmd_que):
    cache_temp=0
    cache_humd=0
    cache_fire=0
    logger.info('<环境> 开启环境信息更新')
    while True:
        try:
            errT,temp_temp,temp_humd=sensor_base.get_temp()
            errF,temp_fire=fire_recog.predict_fire('http://'+str(localhost)+':'+str(vid_port)+'/snapshot')
            if errT:
                cache_temp=temp_temp
                cache_humd=temp_humd
            if errF:
                cache_fire=temp_fire
            sensor2cmd_que((cache_temp,cache_humd,cache_fire))
        except Exception:
            logger.error('<环境> 环境信息获取失败')
        time.sleep(3)
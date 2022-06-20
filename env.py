'''
Author       : Gehrychiang
LastEditTime : 2022-06-20 17:22:08
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import fire_recog
import sensor_base
from loguru import logger
import time
import requests
import json
localhost = '127.0.0.1'
vid_port=18081
def env_core(sensor2cmd_que):
    def pushDeer_push(sk,title,msg):
        server = "https://api2.pushdeer.com"
        endpoint = "/message/push"
        msg=msg+'\n<<此消息推送于：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'>>'
        for it in range(5):
            try:
                ret_json=requests.get(server + endpoint, params={
                        "pushkey": sk,
                        "text": title,
                        "type": 'text',
                        "desp": msg,
                    }).json()
                if ret_json["content"]["result"]:
                    result = json.loads(ret_json["content"]["result"][0])
                    if result["success"] == "ok":
                        break
            except:
                it += 1
    cache_temp=0
    cache_humd=0
    cache_fire=0
    las_warn=0
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
                if cache_fire >=0.80:
                    if time.time()-las_warn>60:
                        pushDeer_push('PDU10571TdF4JjUVAjt7ecGA6lff3jeNCxcWBwUZU', "检测到火灾高风险", '检测到火灾高风险，请确认并排除风险')
                        logger.warning('<环境> 检测到火灾高风险，已发送报警信息')
                        las_warn=time.time()
                    
            sensor2cmd_que.put((cache_temp,cache_humd,cache_fire))
        except Exception:
            logger.error('<环境> 环境信息获取失败')
        time.sleep(3)
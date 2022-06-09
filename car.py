'''
Author       : Gehrychiang
LastEditTime : 2022-06-09 14:50:53
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
from loguru import logger


def car_main(arr_name, cmd_que):
    # shm_ghost = shared_memory.SharedMemory(name=arr_name)
    # img = np.ndarray(shape=(480, 854, 3), dtype=np.uint8, buffer=shm_ghost.buf)
    # init
    logger.debug('车辆动作机构初始化完成')
    running_mode = 1
    # mode 1 2 3
    # 1: manual
    # 2: auto-lane
    # 3: auto-avoid

    motor1_pwm = 0
    motor2_pwm = 0
    motor3_pwm = 0
    motor4_pwm = 0
    while True:
        if not cmd_que.empty():
            cmd = cmd_que.get()
            # cmd 1 2 3 4
            # car ↑ ↓ ← →
            if cmd == 1:
                if running_mode!=1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                logger.debug('车辆加速')
            elif cmd == 2:
                if running_mode!=1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                logger.debug('车辆减速')
            elif cmd == 3:
                if running_mode!=1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                logger.debug('车辆左转')
            elif cmd == 4:
                if running_mode!=1:
                    logger.warning('车辆动作机构已切换到手动模式')
                    running_mode = 1
                # set gpio here
                logger.debug('车辆右转')
            elif cmd == 5:
                running_mode = 1
                # set gpio here
                logger.warning('车辆动作机构已切换到手动模式')
            elif cmd == 6:
                running_mode = 2
                # set gpio here
                logger.warning('车辆动作机构已切换到自动车道模式')
            elif cmd == 7:
                running_mode = 3
                # set gpio here
                logger.warning('车辆动作机构已切换到自动避障模式')

if __name__ == "__main__":
    pass
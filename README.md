<!--
 * @Author       : Gehrychiang
 * @LastEditTime : 2022-06-09 15:22:59
 * @Website      : www.yilantingfeng.site
 * @E-mail       : gehrychiang@aliyun.com
-->
# RaspiCarSolution

## 项目架构图
![](https://pic-static.yilantingfeng.site/imgs/2022/06/09/11-33-12-f80de753777ad3b780ef5752f8f851ff-20220609113311-89ce1e.png)

## 项目日志
2022.6.6 立项，分析项目需求，制定技术栈，指定任务安排

2022.6.7 初步完成GUI界面，结合性能要求，搭建分布式多进程架构体系

2022.6.8 实现摄像头模块，并完成全面性能调优，减少IO瓶颈（摄像头）压力，引入共享内存机制以确保高效执行，进一步完善

2022.6.9 引入日志模块，完善自动回连与等待机制，搭建了车辆的被控线程体系
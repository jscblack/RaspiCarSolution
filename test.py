'''
Author       : Gehrychiang
LastEditTime : 2022-06-12 22:49:46
Website      : www.yilantingfeng.site
E-mail       : gehrychiang@aliyun.com
'''
import json
jsonString='{"cmd":"move","para":{"direction":"left","behavior":"accelerate"}}'
print(jsonString)
obj=json.loads(jsonString)
print(obj['cmd'])
print(obj['para'])
print(obj['para']['direction'])
print(obj['para']['behavior'])
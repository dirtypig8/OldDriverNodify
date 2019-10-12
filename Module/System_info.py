import os
import psutil

# https://blog.csdn.net/xm_csdn/article/details/76947774
# https://www.twblogs.net/a/5bf375a8bd9eee37a0607e03
# https://www.itread01.com/article/1528702710.html
class SystemInfo:
    def __init__(self):
        pass

    def get_cpu_temp(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return (res.replace("temp=","").replace('\'',chr(0xB0)).replace("\n",""))

    def get_memory_usage(self):
        info = psutil.virtual_memory()
        # print('記憶體使用：', psutil.Process(os.getpid()).memory_info().rss)
        # print('總記憶體：', info.total)
        # print('cpu個數：', psutil.cpu_count())
        memory_usage = '{} %'.format(info.percent)
        # print('記憶體使用率：', memory_usage)
        return memory_usage

    def get_cpu_usage(self):
        # print("物理CPU个数: %s" % psutil.cpu_count(logical=False))'
        cpu_usage = '{} %'.format(psutil.cpu_percent(interval=1))
        # print("cup使用率: ", cpu_usage)
        return cpu_usage



if __name__ == '__main__':
    obj = SystemInfo()
    # print(obj.get_cpu_usage())
    # print(obj.get_cpu_temp())
    obj.get_cpu_usage()
    obj.get_memory_usage()

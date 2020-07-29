import time
import json
from threading import Thread
from LogWriter import LogWriter
from Module.Avgle_fn import Avgle
from Module.JavBus_fn import Javbus
from Module.Getrelax import Getrelax
from Module.LineBot import LineNotify
from Module.Seven_mm_fn import Seven_mm
from Module.System_info import SystemInfo
from Module.av01_fn import Av01_fn
from Module.ReurlShorten import ReurlShorten
from Module.BitlyShorten import BitlyShorten
from CoreConfig.ConfigDictionary import ConfigDictionary


class AvLineBot:
    def __init__(self):
        self.config_init()
        self.Javbus_obj = Javbus()
        self.avgle_obj = Avgle()
        self.av01_obj = Av01_fn()
        self.Getrelax = Getrelax()
        self.Seven_mm = Seven_mm()
        self.SystemInfo = SystemInfo()
        self.ReurlShorten = ReurlShorten()
        self.BitlyShorten = BitlyShorten()

        self.linebot = LineNotify(self.line_access_token)
        self.sended_avid_list = []
        self.get_sended_avid()

    def config_init(self):
        self.line_access_token = ConfigDictionary.config_dict['line_access_token']
        self.send_random_avid_to_line_sleep = ConfigDictionary.config_dict['send_random_avid_to_line_sleep']
        self.sync_javbus_sleep = ConfigDictionary.config_dict['sync_javbus_sleep']
        self.send_new_avid_to_line_sleep = ConfigDictionary.config_dict['send_new_avid_to_line_sleep']
        self.send_system_info_to_line_sleep = ConfigDictionary.config_dict['send_system_info_to_line_sleep']

    def get_sended_avid(self):
        try:
            f = open("sended_avid.txt", 'r')
            data = json.load(f)
            f.close()
            self.sended_avid_list = data
        except:
            print('None Find sended_avid.txt')

    def add_sended_avid(self, avid):
        self.sended_avid_list.append(avid)
        f = open("sended_avid.txt", 'w+')
        f.write(json.dumps(self.sended_avid_list))
        f.close()

    def update_sources(self):
        LogWriter().write_log("start execute '{}'".format('sync javbus'))
        try:
            self.linebot.send("例行同步所有資料中......")
            self.Javbus_obj.Scrape_All_Video_Page_Link()
        except:
            LogWriter().write_log('sync javbus error')

        else:
            LogWriter().write_log("end execute '{}'".format('sync javbus'))

    def execute(self):
        while True:
            avid = self.Javbus_obj.get_random_avid()
            if self.__check_sended_list(avid):
                if self.avgle_obj.get_avid_data(avid=avid) is True and \
                        len(self.av01_obj.get_avid_url(avid=avid)) > 0:

                    LogWriter().write_log('start send random avid : {}' .format(avid))
                    self.Javbus_obj.get_avid_data(avid=avid)
                    self.send_message(avid)
                    self.add_sended_avid(avid)
                    LogWriter().write_log('end send random avid : {}'.format(avid))
                    time.sleep(self.send_random_avid_to_line_sleep)

    def send_message(self, avid):
        title = self.avgle_obj.get_avid_information(key="title")
        embedded_key = self.avgle_obj.get_avid_information(key="embedded_url")
        if len(embedded_key[24:]) == 20:
            embedded_key = 'https://7mmtv.tv/iframe_avgle.php?code={}'.format(embedded_key[24:])
        preview_video_url = self.avgle_obj.get_avid_information(key="preview_video_url")
        keyword = self.avgle_obj.get_avid_information(key="keyword")

        img = self.Javbus_obj.get_avid_information(key='img_url')
        genre = self.Javbus_obj.get_avid_information(key='genre')
        Seven_mm_url = self.Seven_mm.get_avid_url(avid)
        av01_url = self.av01_obj.get_avid_url(avid=avid)

        if Seven_mm_url:
            Seven_mm_url = self.__build_shorten(Seven_mm_url)
        like_percent = self.avgle_obj.get_like_percent()
        duration = self.avgle_obj.get_duration()
        add_time = self.avgle_obj.get_add_time()

        message = """
番號: {} / {}
女優: {}
片名: {}
類型: {}
片長: {}分鐘
推薦指數: {}%
        
線上看全片
Avgle全螢幕:
{}

7mm_tv線上看:
{}

av01線上看:
{}

9秒試看:
{}""".format(avid, add_time, keyword, title, genre, duration, like_percent, embedded_key, Seven_mm_url, av01_url, preview_video_url)
        self.linebot.send(message=message, image_url=img)

        return 1

    def get_new_avid(self):
        old_page_one_avid_list = []
        frist_send = 0
        while True:
            LogWriter().write_log('{}'.format('start get new avid'))
            new_page_one_avid_list = self.Javbus_obj.get_page_video(1)
            set_old_page_one_avid_list = set(old_page_one_avid_list)
            set_new_page_one_avid_list = set(new_page_one_avid_list)
            new_avid_list = set_new_page_one_avid_list.difference(set_old_page_one_avid_list)
            old_page_one_avid_list = new_page_one_avid_list
            if new_avid_list and frist_send:
                self.update_sources()
                message = '新片番號通知: '
                for avid in new_avid_list:
                    message = '{}\n{}'.format(message, avid)
                self.linebot.send(message=message)
            else:
                frist_send = 1
                LogWriter().write_log('{}'.format('not find new avid'))
                # print(old_page_one_avid_list)
            LogWriter().write_log('{}'.format('end get new avid'))
            time.sleep(self.send_new_avid_to_line_sleep)

    def __check_sended_list(self, avid):
        if avid in set(self.sended_avid_list):
            LogWriter().write_log('Has be sended avid : {}'.format(avid))
            return 0
        else:
            return 1

    def notify_system_info(self):
        while True:
            cpu_usage = self.SystemInfo.get_cpu_usage()
            memory_usage = self.SystemInfo.get_memory_usage()
            cpu_temp = self.SystemInfo.get_cpu_temp()
            message = """\n------系統狀態------\nCPU溫度: {}\nCPU使用率: {}\n記憶體使用率: {}""".format(cpu_temp, cpu_usage, memory_usage)
            try:
                LogWriter().write_log('start notify system info to line')
                self.linebot.send(message=message)
            except:
                LogWriter().write_log('start notify system info to line error')
            else:
                LogWriter().write_log('end notify system info to line')
            time.sleep(self.send_system_info_to_line_sleep)

    def __build_shorten(self, url):
        # 短網址失敗會回傳原始url
        shorten_url = self.ReurlShorten.build_shorten(url)
        if shorten_url == url:
            shorten_url = self.BitlyShorten.build_shorten(url)
        return shorten_url

    def getrelax_get_new_avid(self):
        while True:
            try:
                LogWriter().write_log('{}'.format('start getrelax get new avid'))
                self.Getrelax.Scrape_All_Video_Page_Link()
                LogWriter().write_log('{}'.format('end getrelax get new avid'))
                time.sleep(43200)
            except:
                LogWriter().write_log('{}'.format('getrelax get new avid error'))

    def getrelax_execute(self):
        while True:
            try:
                avid = self.Getrelax.get_random_avid()
                # result['video_url'] ['img_src'] ['video_name'] ['video_index_url'] ['video_id']
                if avid != '':
                    LogWriter().write_log('start Getrelax random avid : {}' .format(avid['video_name']))
                    message = """
片名: {}

線上看全片
電腦端:
{}

手機端:
{}

本網站目前24小時內只能看5部，持續尋找新片源中
""".format(avid['video_name'], avid['video_index_url'], avid['video_url'])
                    self.linebot.send(message=message, image_url=avid['img_src'])
                    LogWriter().write_log('end send random avid : {}'.format(avid))
                    time.sleep(14400)
            except:
                pass


if __name__ == '__main__':
    threads = []
    Avbot = AvLineBot()
    Avbot.update_sources()
    t1 = Thread(target=Avbot.execute)
    t2 = Thread(target=Avbot.get_new_avid)
    t1.start()
    t2.start()
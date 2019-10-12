import time
import json
from threading import Thread
from Module.Avgle_fn import Avgle
from Module.JavBus_fn import Javbus
from Module.LineBot import LineNotify
from Module.Seven_mm_fn import Seven_mm
from CoreConfig.ConfigDictionary import ConfigDictionary


class AvLineBot:
    def __init__(self):
        self.config_init()
        self.Javbus_obj = Javbus()
        self.avgle_obj = Avgle()
        self.Seven_mm = Seven_mm()
        self.linebot = LineNotify(self.line_access_token)
        self.sended_avid_list = []
        self.get_sended_avid()

    def config_init(self):
        self.line_access_token = ConfigDictionary.config_dict['line_access_token']
        self.send_random_avid_to_line_sleep = ConfigDictionary.config_dict['send_random_avid_to_line_sleep']
        self.sync_javbus_sleep = ConfigDictionary.config_dict['sync_javbus_sleep']
        self.send_new_avid_to_line_sleep = ConfigDictionary.config_dict['send_new_avid_to_line_sleep']

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
        print('START sync_javbus')
        try:
            self.linebot.send("例行同步所有資料中......")
            self.Javbus_obj.Scrape_All_Video_Page_Link()
            print('sync_javbus success.......')
            # time.sleep(self.sync_javbus_sleep)
        except:
            print('sync_javbus error.......')

    def execute(self):
        while True:
            avid = self.Javbus_obj.get_random_avid()
            if self.avgle_obj.get_avid_data(avid=avid) and self.__check_sended_list(avid):
                print('START send_random_avid_to_line  avid : {}' .format(avid))
                self.send_message(avid)
                print('send_random_avid_to_line success..........')
                self.add_sended_avid(avid)
                time.sleep(self.send_random_avid_to_line_sleep)

    def send_message(self, avid):
        title = self.avgle_obj.get_avid_information(key="title")
        embedded_key = self.avgle_obj.get_avid_information(key="embedded_url")
        if len(embedded_key[24:]) == 20:
            embedded_key = 'https://7mmtv.tv/iframe_avgle.php?code={}'.format(embedded_key[24:])
        preview_video_url = self.avgle_obj.get_avid_information(key="preview_video_url")
        keyword = self.avgle_obj.get_avid_information(key="keyword")
        img = self.Javbus_obj.get_avid_img(avid)
        Seven_mm_url = self.Seven_mm.get_avid_url(avid)
        like_percent = self.avgle_obj.get_like_percent()
        duration = self.avgle_obj.get_duration()
        message = """\n番號: {}\n女優: {}\n片名: {}\n片長: {}分鐘\n推薦指數: {}%\n\n線上看全片\nAvgle全螢幕:\n{}\n7mm_tv線上看:\n{}\n\n9秒試看:\n{}"""\
            .format(avid, keyword, title, duration, like_percent, embedded_key, Seven_mm_url, preview_video_url)
        self.linebot.send(message=message, image_url=img)
        return 1

    def get_new_avid(self):
        old_page_one_avid_list = []
        frist_send = 0
        while True:
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
                print('send_new_avid_to_line : 無更新')
                # print(old_page_one_avid_list)
            time.sleep(self.send_new_avid_to_line_sleep)

    def __check_sended_list(self, avid):
        if avid in set(self.sended_avid_list):
            print('{} has been sent'.format(avid))
            return 0
        else:
            return 1


if __name__ == '__main__':
    threads = []
    Avbot = AvLineBot()
    Avbot.update_sources()
    t1 = Thread(target=Avbot.execute)
    t2 = Thread(target=Avbot.get_new_avid)
    t1.start()
    t2.start()
from LineBot import LineNotify
from JavBus_fn import Javbus
from Avgle_fn import Avgle
from threading import Thread
from ConfigsFromFile import *
import time
import random

class Avlinebot:
    def __init__(self):
        self.Javbus_obj = Javbus()
        self.avgle_obj = Avgle()
        self.config_content = ConfigsFromFile('config.ini')
        self.ACCESS_TOKEN = self.config_content.get_config_if_exist('line', 'access_token')
        self.send_random_avid_to_line_sleep = int(self.config_content.get_config_if_exist('system', 'send_random_avid_to_line_sleep'))
        self.sync_javbus_sleep = int(self.config_content.get_config_if_exist('system', 'sync_javbus_sleep'))
        self.send_new_avid_to_line_sleep = int(self.config_content.get_config_if_exist('system', 'send_new_avid_to_line_sleep'))
        self.linebot = LineNotify(self.ACCESS_TOKEN)

    def update_sources(self):
        while True:
            print('START sync_javbus')
            try:
                self.linebot.send("例行同步所有資料中......")
                self.Javbus_obj.Scrape_All_Video_Page_Link()
                print('sync_javbus success.......')
                time.sleep(self.sync_javbus_sleep)
            except:
                print('sync_javbus error.......')

    def execute(self):
        while True:
            avid = self.Javbus_obj.get_random_avid()
            if self.avgle_obj.get_avid_data(avid=avid):
                print('START send_random_avid_to_line  avid : {}' .format(avid))
                title = self.avgle_obj.get_avid_information(key="title")
                embedded_key = self.avgle_obj.get_avid_information(key="embedded_url")
                if len(embedded_key[24:]) == 20:
                    embedded_key = 'https://7mmtv.tv/iframe_avgle.php?code={}'.format(embedded_key[24:])
                preview_video_url = self.avgle_obj.get_avid_information(key="preview_video_url")
                keyword = self.avgle_obj.get_avid_information(key="keyword")
                img = self.Javbus_obj.get_avid_img(avid)
                message = '\n番號: {}\n女優: {}\n片名: {}\n線上看全片:\n {}\n\n試看:\n {}'.format(avid, keyword, title, embedded_key, preview_video_url)
                self.linebot.send(message=message, image_url=img)
                print('send_random_avid_to_line success..........')
                time.sleep(self.send_random_avid_to_line_sleep)

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
                message = '新片番號通知: \n'
                for avid in new_avid_list:
                    message = '{} {}\n'.format(message, avid)
                self.linebot.send(message=message)
            else:
                frist_send = 1
                print('send_new_avid_to_line : 無更新')
            time.sleep(self.send_new_avid_to_line_sleep)


if __name__ == '__main__':
    Avlinebot = Avlinebot()
    t1 = Thread(target=Avlinebot.update_sources)
    t2 = Thread(target=Avlinebot.execute)
    t3 = Thread(target=Avlinebot.get_new_avid)
    t1.start()
    t2.start()
    t3.start()
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
        self.config_content = ConfigsFromFile('config.ini')
        self.ACCESS_TOKEN = self.config_content.get_config_if_exist('line', 'access_token')
        self.linebot = LineNotify(self.ACCESS_TOKEN)

    def update_sources(self):

        while True:
            self.linebot.send("例行同步所有資料中......")
            self.Javbus_obj.Scrape_All_Video_Page_Link()
            time.sleep(14400)

    def execute(self):
        print('start')
        while True:
            avid = self.Javbus_obj.get_random_avid()
            if avid:
                self.linebot.send('------------------------')
                Avgle_obj= Avgle(avid)
                title = Avgle_obj.get_avid_information(key="title")
                embedded_key = Avgle_obj.get_avid_information(key="embedded_url")
                if len(embedded_key[24:]) == 20:
                    embedded_key = 'https://7mmtv.tv/iframe_avgle.php?code={}'.format(embedded_key[24:])
                preview_video_url = Avgle_obj.get_avid_information(key="preview_video_url")
                img = self.Javbus_obj.get_avid_img(avid)

                message = '\n番號: {}\n名稱: {}\n完整連結:\n {}\n\n縮影:\n {}'.format(avid, title, embedded_key, preview_video_url)
                print(message)
                self.linebot.send(message=message, image_url=img)
                time.sleep(600)



if __name__ == '__main__':
    Avlinebot = Avlinebot()
    t1 = Thread(target=Avlinebot.update_sources)
    t2 = Thread(target=Avlinebot.execute)
    t1.start()
    t2.start()

from LineBot import LineNotify
from JavBus_fn import Javbus
from Avgle_fn import Avgle
from ConfigsFromFile import *
import time
import random


if __name__ == '__main__':
    Javbus_obj = Javbus()
    avid_list = Javbus_obj.get_page_video(page_num='1')
    print(avid_list)

    config_content = ConfigsFromFile('config.ini')
    ACCESS_TOKEN = config_content.get_config_if_exist('line', 'access_token')
    bot = LineNotify(ACCESS_TOKEN)
    while avid_list:
        avid = random.choice(avid_list)

        Avgle_obj = Avgle(avid)

        title = Avgle_obj.get_avid_information(key="title")
        embedded_url = Avgle_obj.get_avid_information(key="embedded_url")
        preview_video_url = Avgle_obj.get_avid_information(key="preview_video_url")
        img = Javbus_obj.get_avid_img(avid)

        message = '\n番號: {}\n名稱: {}\n完整連結:\n {}\n\n縮影:\n {}'.format(avid, title, embedded_url, preview_video_url)
        print(message)
        bot.send(message=message,image_url=img)
        time.sleep(10)

import re
import time
import json
import random
import requests
from tqdm import tqdm
from queue import Queue
from threading import Thread
from Module.Net_fn import Net
from bs4 import BeautifulSoup


class Getrelax:
    def __init__(self):
        self.Net = Net()
        self.Video_Page_Queue = Queue()
        self.Video_Page_Scapre_Thread_Num = 2 #最大爬蟲線程數
        self.Video_Page_Thread_List = []
        self.Video_Page_Links = []
        self.video_data = dict()

    def get_page_max_number(self):
        Last_Page_Num = 10
        return int(Last_Page_Num) + 1

    def Thread_Get_Page_Video(self):
        while self.Video_Page_Queue.qsize() != 0:
            Page_Number = self.Video_Page_Queue.get()
            links = self.get_page_video(Page_Number)
            for link in links:
                self.Video_Page_Links.append(link)

            time.sleep(1)

    def Scrape_All_Video_Page_Link(self):
        Page_Max = self.get_page_max_number()
        All_Links = []
        self.Video_Page_Links = []
        for n in tqdm(range(1, Page_Max), desc="正在分配爬行任務"):
            self.Video_Page_Queue.put(n)
            # 加任務

        for n in range(self.Video_Page_Scapre_Thread_Num):
            t = Thread(target=self.Thread_Get_Page_Video)
            t.start()

            self.Video_Page_Thread_List.append(t)

        Total_Mission = self.Video_Page_Queue.qsize()
        while self.Video_Page_Queue.qsize() != 0:
            print("爬蟲進度：{}/{}".format(self.Video_Page_Queue.qsize(),Total_Mission))
            time.sleep(1)

        f = open("Video_Page_Link.txt", 'w+')
        f.write(json.dumps(self.Video_Page_Links))
        f.close()

    def get_random_avid(self):
        try:
            avid = random.choice(self.Video_Page_Links)
            return avid
        except:
            return ''

    def get_page_video(self, page_num):
        video_information = dict()
        video_list = list()
        url = 'https://getrelax.cc/avtag/%E5%8F%B0%E7%81%A3SWAG.html?tag_name=%E5%8F%B0%E7%81%A3SWAG&p={}'.format(page_num)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "authority": "getrelax.cc",
            # "Connection": "close",
            # "X-Requested-With":  "XMLHttpRequest",
            # "Referer": url
        }
        try:
            rs = self.Net.Get(url=url, header=header)
            soup = BeautifulSoup(rs, 'lxml')
            date_tags = soup.find_all('div', attrs={"class": re.compile("grid-boxes-in")})

        except Exception as e:
            pass

        for tag in date_tags:
            try:
                name = tag.find("a")
                if name:
                    # print('----' * 20)
                    # print(tag)
                    # print('----' * 20)
                    embed_url = tag.find("a")["href"]
                    video_id = embed_url[10:16]
                    video_url = 'https://getrelax.cc/embed/{}.mp4'.format(video_id)
                    # print(video_url)

                    video_index_url = "https://getrelax.cc/{}".format(embed_url)
                    session = requests.Session()
                    rs = session.get(url=video_index_url, headers=header)

                    fake_img_src = tag.find("img")["src"]
                    # print(fake_img_src)

                    header_2 = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
                        "referer": video_index_url,
                    }
                    rs = session.get(url=fake_img_src, headers=header_2, allow_redirects=False)
                    # print(rs.headers['Location'])
                    img_src = 'https://static.fanstube.club{}'.format(rs.headers['Location'])
                    # print(img_src)

                    video_name = tag.find("h3").find(target="_blank").get_text()
                    # print(video_name)

                    if video_url != '' and img_src != '' and len(video_name) > 3:
                        result= dict()
                        result['video_id'] = video_id
                        result['video_url'] = video_url
                        result['img_src'] = img_src
                        result['video_name'] = video_name
                        result['video_index_url'] = video_index_url
                        video_information = result.copy()
                        video_list.append(video_information)
            except:
                pass

        return video_list

if __name__ == '__main__':
    obj = Getrelax()
    # print(obj.get_page_video(page_num='2'))
    # print(obj.get_page_video(page_num='1'))
    obj.Scrape_All_Video_Page_Link()
    print(obj.get_random_avid())

import re
import time
import json
import random
from tqdm import tqdm
from queue import Queue
from threading import Thread
from Module.Net_fn import Net
from bs4 import BeautifulSoup


class Javbus:
    def __init__(self):
        self.Net = Net()
        self.Video_Page_Queue = Queue()
        self.Video_Page_Scapre_Thread_Num = 20 #最大爬蟲線程數
        self.Video_Page_Thread_List = []
        self.Video_Page_Links = []

        self.video_data = dict()

    def get_page_video(self, page_num):
        url = 'https://www.javbus.com/page/{}'.format(page_num)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Host": "www.javbus.com",
            "Connection": "close",
            "X-Requested-With":  "XMLHttpRequest",
            "Referer": url
        }

        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        date_tags = soup.find_all('date')

        video_List = []
        avid_pattern = re.compile(r"(\D{1,}-)")
        for tag in date_tags:
            n = avid_pattern.match(tag.string)
            if n:
                video_List.append(tag.string)
        # print(tag_soup)
        return video_List

    def get_avid_information(self, key='title'):
        key_book = ["img_url", "genre"]
        if key in key_book:
            return self.video_data.get(key)
        return 'error key'

    def get_avid_data(self, avid):
        try:
            self.video_data = self.__get_ajax(avid)
            print("get_avid_data success '{}'".format(self.video_data))
            return True
        except Exception as e:
            print("get_avid_data fail '{}'".format(e))
            return False
    def get_avid_magnet_url(self, avid):
        '''获取javbus的磁力链接'''
        video_data = self.__get_ajax(avid)
        url = video_data["ajax"]
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Host": "www.javbus.com",
            "Connection": "close",
            "X-Requested-With":  "XMLHttpRequest",
            "Referer": url
        }
        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        print(soup.prettify())

        avdist = {'title': '', 'magnet': '', 'size': '', 'date': ''}

        for tr in soup.find_all('tr'):
            i = 0
            for td in tr:
                if (td.string):
                    continue
                i = i + 1
                avdist['magnet'] = td.a['href']
                if (i % 3 == 1):
                    avdist['title'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if (i % 3 == 2):
                    avdist['size'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if (i % 3 == 0):
                    avdist['date'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
            print(avdist)
        return avdist

    def __get_ajax(self, avid):
        '''获取javbus的ajax'''

        url = 'https://www.javbus.com/{}'.format(avid)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Host": "www.javbus.com",
            "Connection": "close",
            "X-Requested-With":  "XMLHttpRequest",
            "Referer": url
        }
        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        html = soup.prettify()
        # print(html)
        '''获取img'''
        img_pattern = re.compile(r"var img = '.*?'")
        match = img_pattern.findall(html)
        img = match[0].replace("var img = '", "").replace("'", "")
        # print('封面为', img)

        '''获取uc'''
        uc_pattern = re.compile(r"var uc = .*?;")
        match = uc_pattern.findall(html)
        uc = match[0].replace("var uc = ", "").replace(";", "")

        '''類型'''
        soup_genre_list = soup.find_all("span", {"class": "genre"})
        genre_message = ''
        for genre in soup_genre_list[:-1]:
            if genre_message == '':
                genre_message = genre.find("a").get_text()
            else:
                genre_message = '{},{}'.format(genre_message, genre.find("a").get_text())



        '''获取gid'''
        gid_pattern = re.compile(r"var gid = .*?;")
        match = gid_pattern.findall(html)

        gid = match[0].replace("var gid = ", "").replace(";", "")

        '''获取ajax'''
        ajax = "https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=" + gid + "&lang=zh&img=" + img + "&uc=" + uc

        video_data = {"ajax": ajax, 'img_url': img, 'genre': genre_message}
        return video_data

    def get_page_max_number(self):
        Last_Page_Num = 120
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

    def get_random_genre_video(self, genre):
        while True:
            page = random.randint(1, 100)
            url = 'https://www.javbus.com/genre/{}/{}'.format(genre, page)
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
                "Host": "www.javbus.com",
                "Connection": "close",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": url
            }
            video_List = []
            try:
                rs = self.Net.Get(url=url, header=header)
                soup = BeautifulSoup(rs, 'lxml')
                date_tags = soup.find_all('date')
                avid_pattern = re.compile(r"(\D{1,}-)")

                for tag in date_tags:
                    n = avid_pattern.match(tag.string)
                    if n:
                        video_List.append(tag.string)
            except:
                video_List = []

            if video_List:
                return random.choice(video_List)


if __name__ == '__main__':
    obj = Javbus()
    # print(obj.get_page_video(page_num='1'))
    print(obj.get_avid_data('PRED-198'))
    print(obj.get_avid_information('img_url'))
    print(obj.get_avid_information('genre'))
    # obj.Scrape_All_Video_Page_Link()
    # print(obj.get_random_avid())
    # print(obj.get_random_genre_video(45))
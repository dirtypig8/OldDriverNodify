from bs4 import BeautifulSoup
from Net_fn import Net
import json


class Avgle:
    def __init__(self, avid):
        self.Net = Net()
        self.video_data = {}
        self.__get_avid_data(avid)

    def get_avid_information(self, key='title'):
        key_book = ["title", "keyword", "embedded_url", "preview_video_url"]
        if key in key_book:
            return self.__get_avid_key(key)
        return 'error key'

    def __get_avid_data(self, avid):
        page = 0
        limit = 2
        url = 'https://api.avgle.com/v1/jav/{}/{}?limit={}'.format(avid, page, limit)
        rs = self.Net.Get(url=url)
        self.video_data = json.loads(rs)
        # print(self.video_data)

    def __get_avid_key(self, key):
        response = self.video_data
        if response['success']:
            videos = response['response']['videos']
            # print("avgle返回的videos为：")
            if videos != []:
                # print(videos[0][key])
                return videos[0][key]
            else:
                return "SUCCESS,BUT NOT GET"
        else:
            return "FAIL"

    def getPreview(avid):
        '''avgle.com获取预览视频'''
        AVGLE_SEARCH_JAV_API_URL = 'https://api.avgle.com/v1/jav/{}/{}?limit={}'
        url = AVGLE_SEARCH_JAV_API_URL
        query = avid
        page = 0
        limit = 2
        proxy = urllib.request.ProxyHandler({'https': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        response = json.loads(
            urllib.request.urlopen(url.format(urllib.parse.quote_plus(query), page, limit)).read().decode())
        print(response)
        if response['success']:
            videos = response['response']['videos']
            # print("avgle返回的videos为：")
            if (videos!=[]):
                print(videos[0]["title"])
                # return videos[0]["preview_video_url"]
                return videos
            else:
                return "SUCCESS,BUT NOT GET"
        else:
            return "FAIL"


if __name__ == '__main__':
    # key_book = ["title", "keyword", "embedded_url", "preview_video_url"]
    obj=Avgle('SSNI-563')
    obj.get_avid_information(key="preview_video_url")

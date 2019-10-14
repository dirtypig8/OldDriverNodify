import json
import time
from Module.Net_fn import Net


class Avgle:
    def __init__(self):
        self.Net = Net()
        self.video_data = {}

    def get_avid_information(self, key='title'):
        key_book = ["title", "keyword", "embedded_url", "preview_video_url", "likes", "dislikes", "duration", "addtime"]
        if key in key_book:
            return self.__get_avid_key(key)
        return 'error key'

    def get_avid_data(self, avid):
        page = 0
        limit = 2
        url = 'https://api.avgle.com/v1/jav/{}/{}?limit={}'.format(avid, page, limit)
        try:
            rs = self.Net.Get(url=url)
            self.video_data = json.loads(rs)
            # print(self.video_data)
            return self.video_data['success'] and self.video_data['response']['total_videos']

        except:
            return 0

    def __get_avid_key(self, key):
        response = self.video_data

        if not response['success']:
            return "FAIL"

        videos = response['response']['videos']

        if videos:
            return videos[0][key]
        else:
            return "SUCCESS,BUT NOT GET"

    def get_like_percent(self):
        likes = self.get_avid_information(key = 'likes')
        dislikes = self.get_avid_information(key='dislikes')
        try:
            like_percent = likes / (likes + dislikes) * 100
            return ('%.2f'%like_percent)
        except:
            return 0

    def get_duration(self):
        # 取片長
        second_duration = self.get_avid_information(key='duration')
        try:
            min_duration = second_duration // 60
            return int(min_duration)
        except:
            return '取得失敗'

    def get_add_time(self):
        add_time = self.get_avid_information(key='addtime')
        try:
            timeArray = time.localtime(add_time)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            return otherStyleTime
        except:
            return '取得失敗'


if __name__ == '__main__':
    # key_book = ["title", "keyword", "embedded_url", "preview_video_url"]
    obj = Avgle()
    print(obj.get_avid_data('JUL-001'))

    # obj.get_avid_information(key="preview_video_url")
    title = obj.get_avid_information(key="title")
    like_percent = obj.get_duration()
    get_add_time = obj.get_add_time()
    print(title)
    print(like_percent)
    print(get_add_time)

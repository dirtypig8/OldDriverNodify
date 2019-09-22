import json
from Net_fn import Net


class Avgle:
    def __init__(self):
        self.Net = Net()
        self.video_data = {}

    def get_avid_information(self, key='title'):
        key_book = ["title", "keyword", "embedded_url", "preview_video_url"]
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


if __name__ == '__main__':
    # key_book = ["title", "keyword", "embedded_url", "preview_video_url"]
    obj = Avgle()
    print(obj.get_avid_data('JUY-922'))

    # obj.get_avid_information(key="preview_video_url")
    title = obj.get_avid_information(key="title")
    print(title)

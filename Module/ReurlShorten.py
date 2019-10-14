import json
from Module.Net_fn import Net
from CoreConfig.ConfigDictionary import ConfigDictionary


class ShortenUrl:
    def __init__(self):
        self.key = ConfigDictionary.config_dict['reurl_key']
        self.api_url = 'https://api.reurl.cc/shorten'
        # self.key = '4070df69d794ea3c104b353100ba214de0d7be378d894494ab38acc62b055f6689'
        self.Net = Net()

    def build_shorten(self, rs_url):
        header = {
            "Content-Type": "application/json",
            "reurl-api-key": self.key,
        }
        data = {
            "url": rs_url,
            "utm_source": "FB_AD"
        }
        response = self.Net.Post(url=self.api_url, header=header, data=json.dumps(data))
        response = json.loads(response)
        if response:
            if response["res"] == 'success':
                return response['short_url']
        else:
            return rs_url



if __name__ == '__main__':
    obj = ShortenUrl()
    rs = obj.build_shorten(rs_url='https://www.ptt.cc/bbs/Hearthstone/index.html')
    print(rs)
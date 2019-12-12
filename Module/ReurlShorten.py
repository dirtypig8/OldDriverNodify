import json
from Module.Net_fn import Net
from CoreConfig.ConfigDictionary import ConfigDictionary


class ReurlShorten:
    def __init__(self):
        self.key = ConfigDictionary.config_dict['reurl_key']
        self.api_url = 'https://api.reurl.cc/shorten'
        self.Net = Net()

    def build_shorten(self, url):
        header = {
            "Content-Type": "application/json",
            "reurl-api-key": self.key,
        }
        data = {
            "url": url,
            "utm_source": "FB_AD"
        }
        try:
            response = self.Net.Post(url=self.api_url, header=header, data=json.dumps(data))
            response = json.loads(response)
            if response:
                if response["res"] == 'success':
                    return response['short_url']
            return url

        except Exception as e:
            print("ReurlShorten fail '{}'".format(e))
            return url





if __name__ == '__main__':
    obj = ReurlShorten()
    rs = obj.build_shorten(url='https://www.ptt.cc/bbs/Hearthstone/index.html')
    print(rs)
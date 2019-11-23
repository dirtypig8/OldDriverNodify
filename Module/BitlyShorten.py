import bitly_api
from CoreConfig.ConfigDictionary import ConfigDictionary
#https://github.com/jimmy927/bitly-api-python


class BitlyShorten:
    def __init__(self):
        self.API_USER =  ConfigDictionary.config_dict['bitly_user']
        self.API_KEY =  ConfigDictionary.config_dict['bitly_key']
        self.bitly = bitly_api.Connection(self.API_USER, self.API_KEY)

    def build_shorten(self, url):
        response = self.bitly.shorten(url)
        if response:
            return response['url']
        else:
            return url

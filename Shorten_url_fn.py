import bitly_api
from ConfigsFromFile import *
#https://github.com/jimmy927/bitly-api-python


class Shorten_url:
    def __init__(self):
        self.config_content = ConfigsFromFile('config.ini')
        self.API_USER = self.config_content.get_config_if_exist('bitly', 'API_USER')
        self.API_KEY = self.config_content.get_config_if_exist('bitly', 'API_KEY')

    def build_shorten(self, url):

        bitly = bitly_api.Connection(self.API_USER, self.API_KEY)
        response = bitly.shorten(url)
        if response:
            return response['url']
        else:
            return url

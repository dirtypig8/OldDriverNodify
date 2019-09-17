from bs4 import BeautifulSoup
from Net_fn import Net
from Shorten_url_fn import Shorten_url
import urllib.parse
import json

class Seven_mm:
    def __init__(self):
        self.Net = Net()
        self.short_url = Shorten_url()

    def __bulid_shorten(self, url):
        rs = self.short_url.bulid_shorten(url)
        return rs

    def get_avid_url(self, avid):
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        url = 'https://7mmtv.tv/zh/searchform_search/all/index.html'
        postData = {
            "search_keyword": avid,
            "search_type": "censored",
            "op": "search"
        }
        rs = self.Net.Post(url, data=postData, header=headers)
        soup = BeautifulSoup(rs.text, "lxml")
        try:
            avid_url = soup.find_all("", {"class":"latest-korean-box-text"})[0].find("a")["href"]
            avid_url = urllib.parse.quote(avid_url, safe='://')
            avid_url = self.__bulid_shorten(avid_url)
        except:
            avid_url = 'Not Get'
        return avid_url


if __name__ == '__main__':
    print(Seven_mm().get_avid_url('XXXXX'))
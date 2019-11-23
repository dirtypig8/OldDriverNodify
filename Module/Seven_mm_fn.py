import urllib.parse
from Module.Net_fn import Net
from bs4 import BeautifulSoup


class Seven_mm:
    def __init__(self):
        self.Net = Net()

    def get_avid_url(self, avid):
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        url = 'https://7mmtv.tv/zh/searchform_search/all/index.html'
        postData = {
            "search_keyword": avid,
            "search_type": "censored",
            "op": "search"
        }

        try:
            rs = self.Net.Post(url, data=postData, header=headers)
            soup = BeautifulSoup(rs, "lxml")
            avid_url = soup.find_all("", {"class":"latest-korean-box-text"})[0].find("a")["href"]
            avid_url = urllib.parse.quote(avid_url, safe='://')

        except Exception as e:
            print("Seven_mm fail '{}'".format(e))
            return 0
        else:
            return avid_url


if __name__ == '__main__':
    while 1:
        url = Seven_mm().get_avid_url('ARM-813')
        print(url)
import urllib.parse
from Module.Net_fn import Net
from bs4 import BeautifulSoup
from LogWriter import LogWriter
import requests


class Av01_fn:
    def __init__(self):
        pass

    def get_avid_url(self, avid):
        url = 'https://www.av01.tv/search/videos?search_query={}'.format(avid)

        try:
            response = requests.get(url=url, verify=False, timeout=60)
        except Exception as e:
            LogWriter().write_log("get avgle avid data {} fail, server exception".format(avid, e))
            return ''
        else:
            if response.status_code == requests.codes.ok:
                try:
                    soup = BeautifulSoup(response.text, "lxml")
                    avid_url = soup.find(rel="prefetch").get('href')
                    avid_number = avid_url[7:12]
                    avid_url = 'https://www.av01.tv/video/{}/{}'.format(avid_number, avid)
                    return avid_url

                except Exception as e:
                    return ''
            return ''


if __name__ == '__main__':
    obj = Av01_fn()

    result = obj.get_avid_url('SQTE-316')
    print(result)
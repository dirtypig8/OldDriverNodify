import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Net:
    def __init__(self):
        pass

    def Get(self, url, header="", cookie="", verify=False):

        rs = requests.get(url, headers=header, cookies=cookie, verify=verify)
        rs = rs.text

        return rs

    def Post(self, url, header="", data="", verify=False):

        rs = requests.post(url, data=data, headers=header, verify=verify)
        rs = rs.text

        return rs

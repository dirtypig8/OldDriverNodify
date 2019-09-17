import urllib.request
import urllib.parse
import requests
import json

class Net:
    def __init__(self):
        pass

    def Get(self, url, header=""):
        # proxy_addr = "200.165.72.98:32346"
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        # proxy = urllib.request.ProxyHandler({'https': proxy_addr})
        # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        opener.addheaders = header
        urllib.request.install_opener(opener)
        rs = urllib.request.urlopen(url).read().decode('utf-8')

        return rs

    def Post(self, url, header="", data=""):

        rs = requests.post(url, data=data, headers=header)

        return rs
from bs4 import BeautifulSoup
from Net_fn import Net
import re


class Javbus:
    def __init__(self):
        self.Net = Net()

    def get_page_video(self, page_num):
        url = 'https://www.javbus.com/page/{}'.format(page_num)
        header = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
            ('Host', 'www.javbus.com'),
            ('Connection', 'close'),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Referer', url)
        ]

        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        date_tags = soup.find_all('date')

        tag_soup = []
        avid_pattern = re.compile(r"(\D{1,}-)")
        for tag in date_tags:
            n = avid_pattern.match(tag.string)
            if n:
                tag_soup.append(tag.string)
        # print(tag_soup)
        return tag_soup

    def get_avid_img(self, avid):
        video_data = self.__get_ajax(avid)
        print(video_data['img'])
        return video_data['img']

    def get_avid_magnet_url(self, avid):
        '''获取javbus的磁力链接'''
        video_data = self.__get_ajax(avid)
        url = video_data["ajax"]
        header = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
            ('Host', 'www.javbus.com'),
            ('Connection', 'close'),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Referer', url)
        ]
        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        print(soup.prettify())

        avdist = {'title': '', 'magnet': '', 'size': '', 'date': ''}

        for tr in soup.find_all('tr'):
            i = 0
            for td in tr:
                if (td.string):
                    continue
                i = i + 1
                avdist['magnet'] = td.a['href']
                if (i % 3 == 1):
                    avdist['title'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if (i % 3 == 2):
                    avdist['size'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if (i % 3 == 0):
                    avdist['date'] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
            print(avdist)
        return avdist

    def __get_ajax(self, avid):
        '''获取javbus的ajax'''

        url = 'https://www.javbus.com/{}'.format(avid)
        header = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
            ('Host', 'www.javbus.com'),
            ('Connection', 'close'),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Referer', url)
        ]
        rs = self.Net.Get(url=url, header=header)
        soup = BeautifulSoup(rs, 'lxml')
        html = soup.prettify()
        # print(html)
        '''获取img'''
        img_pattern = re.compile(r"var img = '.*?'")
        match = img_pattern.findall(html)
        img = match[0].replace("var img = '", "").replace("'", "")
        # print('封面为', img)

        '''获取uc'''
        uc_pattern = re.compile(r"var uc = .*?;")
        match = uc_pattern.findall(html)
        uc = match[0].replace("var uc = ", "").replace(";", "")

        '''获取gid'''
        gid_pattern = re.compile(r"var gid = .*?;")
        match = gid_pattern.findall(html)

        gid = match[0].replace("var gid = ", "").replace(";", "")

        '''获取ajax'''
        ajax = "https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=" + gid + "&lang=zh&img=" + img + "&uc=" + uc

        video_data = {"ajax": ajax, 'img': img}
        return video_data




if __name__ == '__main__':
    obj = Javbus()
    # obj.get_page_video(page_num='1')
    obj.get_avid_img('SSNI-563')
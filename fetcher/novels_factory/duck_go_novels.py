#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import asyncio

from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from fetcher.function import get_random_user_agent
from fetcher.novels_factory.base_novels import BaseNovels


class DuckGoNovels(BaseNovels):

    def __init__(self):
        super(DuckGoNovels, self).__init__()

    def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        try:
            title = html.select('h2 a')[0].get_text()
            url = html.select('h2 a')[0].get('href', None)
            url = parse_qs(url).get('uddg', ['#'])[0]
            netloc = urlparse(url).netloc
            url = url.replace('index_demo.html', '').replace('Index.html', '')
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain or '.html' in url:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            # time = html.select('div.b_attribution')[0].get_text()
            # time = re.findall(r'\d+-\d+-\d+', time)
            # time = time[0] if time else ''
            timestamp = 0
            time = ''
            return {'title': title,
                    'url': url,
                    'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}

        except Exception as e:
            self.logger.exception(e)
            return None

    def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        url = self.config.DUCKGO_URL
        headers = {
            'user-agent': get_random_user_agent(),
            'referer': "https://duckduckgo.com/"
        }
        data = {'q': novels_name, 'b': ''}
        html = self.fetch_url(url=url, data=data, headers=headers, method='POST')
        print(html)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='result')
            extra_tasks = [self.data_extraction(html=i) for i in result]
            return extra_tasks
        else:
            return []


def start(novels_name):
    """
    Start spider
    :return:
    """
    return DuckGoNovels.start(novels_name)


if __name__ == '__main__':
    # Start
    novels_name = "{name} 小说 最新章节".format(name='捡破烂成全球首富')
    res = start(novels_name)
    # res = start('捡破烂成全球首富 小说 最新章节')
    print(res)
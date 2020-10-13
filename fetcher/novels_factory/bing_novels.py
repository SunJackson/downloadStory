#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from fetcher.cache import get_the_latest_chapter
from fetcher.function import get_random_user_agent
from fetcher.novels_factory.base_novels import BaseNovels


class BingNovels(BaseNovels):

    def __init__(self):
        super(BingNovels, self).__init__()

    def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        try:
            title = html.select('h2 a')[0].get_text()
            url = html.select('h2 a')[0].get('href', None)
            netloc = urlparse(url).netloc
            url = url.replace('index.html', '').replace('Index.html', '')
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain or '.html' in url:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            latest_chapter_res = get_the_latest_chapter(url)
            latest_chapter_name = latest_chapter_res.get('latest_chapter_name') if latest_chapter_res else '未知'
            return {'title': title,
                    'url': url,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'latest_chapter_name': latest_chapter_name,
                    'netloc': netloc}

        except Exception as e:
            self.logger.exception(e)
            return None

    def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        url = self.config.BY_URL
        headers = {
            'user-agent': get_random_user_agent(),
        }
        params = {'q': novels_name}
        html = self.fetch_url(url=url, params=params, headers=headers)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='b_algo')
            extra_tasks = [self.data_extraction(html=i) for i in result]
            return extra_tasks
        else:
            return []


def start(novels_name):
    """
    Start spider
    :return:
    """
    return BingNovels.start(novels_name)


if __name__ == '__main__':
    # Start
    novels_name = "{name} 小说 阅读 最新章节".format(name='捡破烂成全球首富')
    print(novels_name)
    # b_str = bytes(novels_name, encoding='unicode_escape')
    # h_u_s = b_str.hex()
    # print(h_u_s)
    # b_str = bytes('捡破烂成全球首富 小说 最新章节', encoding='unicode_escape')
    # h_u_s = b_str.hex()
    # print(h_u_s)
    res = start(novels_name)
    # res = start('捡破烂成全球首富 小说 最新章节')
    print(res)

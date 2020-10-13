#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from fetcher.function import get_random_user_agent
from fetcher.novels_factory.base_novels import BaseNovels


class SoNovels(BaseNovels):

    def __init__(self):
        super(SoNovels, self).__init__()

    def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        try:
            # 2017.09.09 修改 更加全面地获取title && url
            try:
                title = html.select('h3 a')[0].get_text()
                url = html.select('h3 a')[0].get('href', None)
            except Exception as e:
                self.logger.exception(e)
                return None

            # 针对不同的请进行url的提取
            if "www.so.com/link?m=" in url:
                url = html.select('h3 a')[0].get('data-mdurl', None)
            if "www.so.com/link?url=" in url:
                url = parse_qs(urlparse(url).query).get('url', None)
                url = url[0] if url else None

            netloc = urlparse(url).netloc
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            new_chapter = html.select('.res-desc a')
            latest_chapter_name = new_chapter[0].get_text() if new_chapter else '未知'
            return {'title': title,
                    'url': url.replace('index.html', '').replace('Index.html', ''),
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
        url = self.config.SO_URL

        headers = {
            'User-Agent': get_random_user_agent(),
            'Referer': "http://www.so.com/haosou.html?src=home"
        }
        params = {'ie': 'utf-8', 'src': 'noscript_home', 'shb': 1, 'q': novels_name, }
        html = self.fetch_url(url=url, params=params, headers=headers)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='res-list')
            extra_tasks = [self.data_extraction(html=i) for i in result]

            return extra_tasks
        else:
            return []


def start(novels_name):
    """
    Start spider
    :return:
    """
    return SoNovels.start(novels_name)


if __name__ == '__main__':
    # Start
    res = start('捡破烂成全球首富 小说 最新章节')
    print(res)
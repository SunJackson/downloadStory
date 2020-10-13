#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fetcher.function import get_random_user_agent
from fetcher.novels_factory.base_novels import BaseNovels


class BaiduNovels(BaseNovels):

    def __init__(self):
        super(BaiduNovels, self).__init__()

    def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        try:
            url = html.select('h3.t a')[0].get('href', None)
            real_url = self.get_real_url(url=url) if url else None
            if real_url:
                real_str_url = str(real_url)
                netloc = urlparse(real_str_url).netloc
                if "http://" + netloc + "/" == real_str_url:
                    return None
                if 'baidu' in real_str_url or netloc in self.black_domain:
                    return None
                is_parse = 1 if netloc in self.rules.keys() else 0

                title = html.select('h3.t a')[0].get_text()

                new_chapter = html.select('p.c-gray a')
                latest_chapter_name = new_chapter[0].get_text() if new_chapter else '未知'

                is_recommend = 1 if netloc in self.latest_rules.keys() else 0

                return {'title': title,
                        'url': real_str_url.replace('index.html', ''),
                        'is_parse': is_parse,
                        'is_recommend': is_recommend,
                        'latest_chapter_name': latest_chapter_name,
                        'netloc': netloc}
            else:
                return None
        except Exception as e:
            return None

    def get_real_url(self, url):
        """
        获取百度搜索结果真实url
        :param url:
        :return:
        """
        try:
            headers = {'user-agent': get_random_user_agent()}
            response = httpx.get(url,  allow_redirects=True, verify=False)
            self.logger.info('Parse url: {}'.format(response.url))
            url = response.url if response.url else None
            return url
        except Exception as e:
            self.logger.exception(e)
            return None

    def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        url = self.config.URL_PC
        params = {'wd': novels_name, 'ie': 'utf-8', 'rn': self.config.BAIDU_RN, 'vf_bl': 1}
        headers = {'user-agent': get_random_user_agent()}
        html = self.fetch_url(url=url, params=params, headers=headers)
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
    return BaiduNovels.start(novels_name)


if __name__ == '__main__':
    # Start
    res = start('捡破烂成全球首富 最新 章节')
    print(res)
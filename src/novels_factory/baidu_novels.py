#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
from bs4 import BeautifulSoup
from src.function import get_random_user_agent
from src.novels_factory.base_novels import BaseNovels


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
            if url:
                title = html.select('h3.t a')[0].get_text()
                return {'title': title,
                        'url': url,
                        'source': '百度'
                        }
            else:
                return None
        except Exception as e:
            return None

    def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        url = 'http://www.baidu.com/s'
        params = {'wd': novels_name, 'ie': 'utf-8', 'rn': 15, 'vf_bl': 1}
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
#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import cchardet
from config import CONFIG, LOGGER, BLACK_DOMAIN
import httpx


class BaseNovels:
    """
    小说抓取父类
    """

    def __init__(self, logger=None):
        self.black_domain = BLACK_DOMAIN
        self.config = CONFIG
        self.logger = logger if logger else LOGGER

    def fetch_url(self, url, params=None, headers=None, data=None, method='GET'):
        """
        公共抓取函数
        :param client:
        :param url:
        :param params:
        :return:
        """
        try:
            response = httpx.request(method=method, url=url, params=params, data=data, headers=headers, timeout=60,
                                     allow_redirects=True)
            assert response.status_code == 200
            LOGGER.info('Task url: {}'.format(response.url))
            content = response.content
            charset = cchardet.detect(content)
            html_doc = content.decode(charset['encoding'])
            return html_doc
        except Exception as e:
            LOGGER.exception(e)
            return None

    @classmethod
    def start(cls, novels_name):
        return cls().novels_search(novels_name)

    def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        raise NotImplementedError

    def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        raise NotImplementedError

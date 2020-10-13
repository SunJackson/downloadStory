#!/usr/bin/env python
import os


class Config():
    """
    Basic config for downloadStory
    """

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'


    # Engine config
    URL_PHONE = 'https://m.baidu.com/s'
    URL_PC = 'http://www.baidu.com/s'
    BAIDU_RN = 15
    SO_URL = "https://www.so.com/s"
    BY_URL = "https://cn.bing.com/search"

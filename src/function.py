#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import os
import random
import re
import aiofiles
import time
import cchardet
import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse, urlunparse
from posixpath import normpath
import urllib3
from importlib import import_module

from config.rules import REPLACE_HTML_STRING

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_data(filename, default='') -> list:
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(os.path.dirname(__file__))
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
        with aiofiles.open(user_agents_file, mode='r') as f:
            data = [_.strip() for _ in f.readlines()]
    except:
        data = [default]
    return data


def get_novels_info(class_name, novels_name):
    novels_module = import_module(
        "src.{}.{}_novels".format('novels_factory', class_name))
    # 获取对应渠道实例化对象

    novels_info = novels_module.start(novels_name)
    return novels_info


def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    ua = UserAgent()
    return ua.random


def get_netloc(url):
    """
    获取netloc
    :param url: 
    :return:  netloc
    """
    netloc = urlparse(url).netloc
    return netloc or None


def urlJoin(base, url):
    '''
    url 拼接
    url = 'http://karpathy.github.io/2014/07/03/feature-learning-escapades/'
    url_join(url, '../assets/nips2012.jpeg')
    'http://karpathy.github.io/2014/07/03/assets/nips2012.jpeg'
    url_join(url, './assets/nips2012.jpeg')
    'http://karpathy.github.io/2014/07/03/feature-learning-escapades/assets/nips2012.jpeg'
    url_join(url, '/assets/nips2012.jpeg')
    'http://karpathy.github.io/assets/nips2012.jpeg'
    url_join(url,'http://karpathy.github.io/assets/nips2012.jpeg')
    'http://karpathy.github.io/assets/nips2012.jpeg'
    '''
    if get_netloc(url):
        return url
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


def remove_html_tags(content):
    content_list = []
    dr = re.compile(r'<[^>]+>', re.S)
    for i in dr.split(str(content)):
        i = i.strip()
        if i.strip():
            for remove_str in REPLACE_HTML_STRING:
                i = i.replace(remove_str, '')
            content_list.append(i)
    return '\n'.join(content_list)


def get_all_div(html):
    new_list = []
    div_list = re.findall('<div .*?>(.*?)</div>', html.replace('\n', ''))
    if div_list:
        for i in div_list:
            new_list.extend(get_all_div(i))
    else:
        new_list.append(html)
    return new_list


def get_baidu_real_url(url):
    """
    获取百度搜索结果真实url
    :param url:
    :return:
    """
    try:
        import time
        headers = {'user-agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True, verify=False, timeout=5)
        url = response.url if response.url else None
        return url
    except Exception as e:
        return None


def get_html_by_requests(url, headers, timeout=15, random_sleep=-1, proxies=None):
    """
    :param url:
    :return:
    """
    text = None
    real_url = None
    status = 0
    try:
        response = requests.get(url=url, headers=headers, allow_redirects=True, verify=False, timeout=timeout,
                                proxies=proxies)
        content = response.content
        status = response.status_code
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        real_url = response.url if response.url else None
    except Exception as e:
        pass

    if random_sleep < 0:
        time.sleep(random.randint(0, 5) / 10)
    if random_sleep > 0:
        time.sleep(random_sleep)
    return text, real_url, status


def check_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print('创建文件夹：{}'.format(path))

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
from urllib.parse import urljoin, urlparse, urlunparse
from posixpath import normpath
import urllib3
from importlib import import_module

from story_dl.rules import REPLACE_HTML_STRING

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
        "story_dl.{}.{}_novels".format('novels_factory', class_name))
    # 获取对应渠道实例化对象

    novels_info = novels_module.start(novels_name)
    return novels_info


def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    useragent = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
    ]
    return random.choice(useragent)


def get_netloc(url):
    """
    获取netloc
    :param url: 
    :return:  netloc
    """
    netloc = urlparse(url).netloc
    return netloc or None


def min_distance(word1: str, word2: str) -> int:
    """
    计算最短编辑距离
    :param word1:
    :param word2:
    :return:
    """
    m, n = len(word1), len(word2)
    dp = [[-1] * (n + 1) for _ in range(m + 1)]

    def dp_dist(i, j):
        if dp[i][j] >= 0:
            return dp[i][j]
        if i * j == 0:
            dp[i][j] = i + j
        elif word1[i - 1] == word2[j - 1]:
            dp[i][j] = dp_dist(i - 1, j - 1)
        else:
            dp[i][j] = 1 + min(dp_dist(i - 1, j), dp_dist(i, j - 1), dp_dist(i - 1, j - 1))
        return dp[i][j]
    return dp_dist(m, n)



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


if __name__ == '__main__':
    res = min_distance('bbbaaaabaabaaaaa', 'bbbaaaabaaaaaabaaaa')
    print(res)
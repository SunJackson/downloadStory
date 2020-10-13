#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

import os
import random

import aiofiles
import time
import cchardet
import httpx

from urllib.parse import urlparse

from config import LOGGER, CONFIG


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


def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(_get_data('user_agents.txt', CONFIG.USER_AGENT))


def get_netloc(url):
    """
    获取netloc
    :param url: 
    :return:  netloc
    """
    netloc = urlparse(url).netloc
    return netloc or None


def get_html_by_requests(url, headers, timeout=15):
    """
    :param url:
    :return:
    """
    try:
        response = httpx.get(url=url, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
        content = response.content
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        time.sleep(random.randint(0, 20) / 10)
        return text
    except Exception as e:
        LOGGER.exception(e)
        time.sleep(random.randint(0, 20) / 10)
        return None

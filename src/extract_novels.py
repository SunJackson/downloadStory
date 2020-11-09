#!/usr/bin/env python
"""
 Created by howie.hu.
"""

from bs4 import BeautifulSoup
import re

from config.rules import CHAPTER_TAG
from src.function import get_html_by_requests, get_random_user_agent, remove_html_tags, urlJoin, get_netloc, \
    get_all_div, min_distance


def get_novels_content(url, **kwargs):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }
    max_content = ''
    html, real_url, status = get_html_by_requests(headers=headers, url=url, **kwargs)
    if html:
        div_content_list = []
        for i in get_all_div(html.replace('\n', '')):
            div_content_list.append(remove_html_tags(i))
        max_content = max(div_content_list, key=len, default='')
    return max_content, status


def get_novels_chapter(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }
    html, real_url, _ = get_html_by_requests(url=url, headers=headers, random_sleep=0)
    data = dict()
    if html:
        try:
            soup = BeautifulSoup(html, 'html5lib')
        except Exception as e:
            return data
        content = []
        for tag in CHAPTER_TAG:
            find_tag = soup.find_all(tag)
            if find_tag:
                content.extend(find_tag)
        # 防止章节被display:none
        if content:
            story_list = []
            for detail_info in content:
                name = (detail_info.get('title', '') or detail_info.get_text()).strip()
                href = detail_info.get('href', '').strip()
                if name and href:
                    content_url = urlJoin(real_url, href.replace('\n', ''))
                    if (name, content_url) in story_list:
                        story_list.remove((name, content_url))
                    story_list.append((name, content_url))
                else:
                    continue
            # 去除杂乱数据
            res_list = []
            processed_url_list = [re.sub('\d+', '*', i[1]) for i in story_list]
            max_url = max(processed_url_list, key=processed_url_list.count)
            len_max_url = len(max_url.split('/'))
            for index, item in enumerate(processed_url_list):
                if  min_distance(item, max_url) < 2 and len(item.split('/')) == len_max_url:
                    res_list.append(story_list[index])
            if res_list:
                data['latest_chapter_name'] = res_list[-1][0]
                data['result'] = res_list
                data['netloc'] = get_netloc(real_url)
    return data


if __name__ == '__main__':
    url = 'https://www.taiuu.com/0/67/'
    res = get_novels_chapter(url)
    print(res)

#!/usr/bin/env python
"""
 Created by howie.hu.
"""

import re
from urllib import parse
from bs4 import BeautifulSoup


from fetcher.function import get_html_by_requests, get_random_user_agent, remove_html_tags,urlJoin
from config import LOGGER


def get_novels_content(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }
    data = dict()
    html,netloc = get_html_by_requests(headers=headers, url=url)
    if html:
        div_list = re.findall('<div .*?>(.*?)</div>', html.replace('\n', ''))
        div_content_list = []
        for i in div_list:
            div_content_list.append(remove_html_tags(i))
        max_content = max(div_content_list, key=len, default='')
        data = {
            'content': max_content,
        }
    return data


def get_novels_chapter(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }

    html, netloc = get_html_by_requests(url=url, headers=headers, random_sleep=0)
    data = dict()
    if html:
        try:
            soup = BeautifulSoup(html, 'html5lib')
        except Exception as e:
            LOGGER.exception(e)
            return data
        content = soup.find_all('a')
        # 防止章节被display:none
        if content:
            story_list = []
            for detail_info in content:
                name = (detail_info.get('title', '') or detail_info.get_text()).strip()
                href = detail_info.get('href', '').strip()

                if name and href:
                    content_url = urlJoin(url, href.replace('\n', ''))
                    if (name, content_url) in story_list:
                        story_list.remove((name, content_url))
                    story_list.append((name, content_url))
                else:
                    continue
            # 去除杂乱数据
            if len(story_list) > 30:
                title_list = [len(i[1]) for i in story_list]
                mean_title = sum(title_list) / len(title_list)
                title_diff_list = [abs(len(i[1]) - mean_title) for i in story_list]
                maxlabel = max(title_diff_list, key=title_diff_list.count)
                remove_list = []
                for item in story_list:
                    if abs(len(item[1]) - mean_title) > maxlabel:
                        remove_list.append(item)
                if remove_list:
                    for i in remove_list:
                        story_list.remove(i)
            if story_list:
                data['latest_chapter_name'] = story_list[-1][0]
                data['result'] = story_list
                data['netloc'] = netloc
    return data


if __name__ == '__main__':
    url = 'https://www.taiuu.com/0/67/'
    res = get_novels_chapter(url)
    print(res)

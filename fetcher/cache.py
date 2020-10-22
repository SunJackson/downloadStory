#!/usr/bin/env python
"""
 Created by howie.hu.
"""

import re
from urllib import parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.tools import ChineseNumToArab
from fetcher.function import get_html_by_requests, get_random_user_agent,get_netloc
from fetcher.extract_novels import extract_pre_next_chapter
from config import RULES, LATEST_RULES, LOGGER


def get_novels_content(url, netloc):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }
    data = dict()
    html = get_html_by_requests(headers=headers, url=url)
    if html:
        soup = BeautifulSoup(html, 'html5lib')
        selector = RULES[netloc].content_selector

        if selector.get('id', None):
            content = soup.find_all(id=selector['id'])
        elif selector.get('class', None):
            content = soup.find_all(class_=selector['class'])
        else:
            content = soup.find_all(selector.get('tag'))
        if content:
            # 提取出真正的章节标题
            title_reg = r'(第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集]\s*.*?)[_,-]'
            title = soup.title.string
            extract_title = re.findall(title_reg, title, re.I)
            if extract_title:
                title = extract_title[0]
            else:
                title = soup.select('h1')[0].get_text()
            if not title:
                title = soup.title.string
            next_chapter = extract_pre_next_chapter(chapter_url=url, html=str(soup))
            content_list = []
            for lines in content:

                if lines and lines.get_text().strip():
                    dr = re.compile(r'<[^>]+>', re.S)
                    for i in dr.split(str(lines)):
                        if i.strip():
                            content_list.append(i.strip())
            data = {
                'content': '\n'.join(content_list),
                'next_chapter': next_chapter,
                'title': title
            }
    return data


def get_novels_chapter(url, netloc):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }

    html = get_html_by_requests(url=url, headers=headers)
    data = dict()
    if html:
        try:
            soup = BeautifulSoup(html, 'html5lib')
        except Exception as e:
            LOGGER.exception(e)
            return data
        latest_chapter_name = None
        if LATEST_RULES[netloc].plan:
            meta_value = LATEST_RULES[netloc].meta_value
            latest_chapter_name = soup.select(
                'meta[property="{0}"]'.format(meta_value["latest_chapter_name"])) or soup.select(
                'meta[name="{0}"]'.format(meta_value["latest_chapter_name"]))

            latest_chapter_name = latest_chapter_name[0].get('content',
                                                             None) if latest_chapter_name else None
        else:
            selector = LATEST_RULES[netloc].selector
            if selector.get('id', None):
                latest_chapter_soup = soup.find_all(id=selector['id'])
            elif selector.get('class', None):
                latest_chapter_soup = soup.find_all(class_=selector['class'])
            else:
                latest_chapter_soup = soup.select(selector.get('tag'))
            if latest_chapter_soup:
                latest_chapter_name = latest_chapter_soup[0].get('title', None)
        if latest_chapter_name:
            data = {
                "latest_chapter_name": latest_chapter_name
            }
        selector = RULES[netloc].chapter_selector
        if selector.get('id', None):
            content = soup.select('#{} a'.format(selector['id']))
        elif selector.get('class', None):
            content = soup.select('.{} a'.format(selector['class']))
        else:
            content = soup.find_all(selector.get('tag'))
        # 防止章节被display:none
        if content:
            title_reg = r'第([一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*)[章回卷节折篇幕集]'
            story_map = dict()
            for detail_info in content:
                re_name = re.findall(title_reg, detail_info.get('title', '') + detail_info.get_text(), re.I)
                if re_name:
                    story_map[int(ChineseNumToArab(re_name[0]))] = (detail_info.get_text().strip(), parse.urljoin(url, detail_info.get('href')))
                else:
                    continue
            res = dict()
            for i in sorted(story_map):
                res[i] = story_map[i]
            data['result'] = res
    return data


def get_the_latest_chapter(chapter_url, timeout=15):
    try:
        data = {}
        if chapter_url:
            url = chapter_url
            netloc = urlparse(url).netloc
            if netloc in LATEST_RULES.keys():
                headers = {
                    'User-Agent': get_random_user_agent(),
                    'Referer': url
                }
                try:
                    html = get_html_by_requests(url=url, headers=headers, timeout=timeout)
                except TypeError:
                    html = get_html_by_requests(url=url, headers=headers, timeout=timeout)
                except Exception as e:
                    LOGGER.exception(e)
                    return None
                try:
                    soup = BeautifulSoup(html, 'html5lib')
                except Exception as e:
                    LOGGER.exception(e)
                    return None
                latest_chapter_name, latest_chapter_url = None, None
                if LATEST_RULES[netloc].plan:
                    meta_value = LATEST_RULES[netloc].meta_value
                    latest_chapter_name = soup.select(
                        'meta[property="{0}"]'.format(meta_value["latest_chapter_name"])) or soup.select(
                        'meta[name="{0}"]'.format(meta_value["latest_chapter_name"]))

                    latest_chapter_name = latest_chapter_name[0].get('content',
                                                                     None) if latest_chapter_name else None
                    latest_chapter_url = soup.select(
                        'meta[property="{0}"]'.format(meta_value["latest_chapter_url"])) or soup.select(
                        'meta[name="{0}"]'.format(meta_value["latest_chapter_url"]))
                    latest_chapter_url = urljoin(chapter_url, latest_chapter_url[0].get('content',
                                                                                        None)) if latest_chapter_url else None
                else:
                    selector = LATEST_RULES[netloc].selector
                    content_url = selector.get('content_url')
                    if selector.get('id', None):
                        latest_chapter_soup = soup.find_all(id=selector['id'])
                    elif selector.get('class', None):
                        latest_chapter_soup = soup.find_all(class_=selector['class'])
                    else:
                        latest_chapter_soup = soup.select(selector.get('tag'))
                    if latest_chapter_soup:
                        if content_url == '1':
                            # TODO
                            pass
                        elif content_url == '0':
                            # TODO
                            pass
                        else:
                            latest_chapter_url = content_url + latest_chapter_soup[0].get('href', None)
                        latest_chapter_name = latest_chapter_soup[0].get('title', None)
                if latest_chapter_name and latest_chapter_url:
                    data = {
                        "latest_chapter_name": latest_chapter_name,
                        "latest_chapter_url": latest_chapter_url
                    }
        return data
    except Exception as e:
        LOGGER.exception(e)
        return None


if __name__ == '__main__':
    url = 'https://www.mmmli.com/book/7/7196/'
    netloc = get_netloc(url)
    res = get_novels_chapter(url, netloc)
    print(res)

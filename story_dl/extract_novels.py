#!/usr/bin/env python
"""
 Created by howie.hu.
"""

from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from operator import itemgetter


from story_dl.rules import CHAPTER_TAG, RULES,CONTENT_REPLACE
from story_dl.function import get_html_by_requests, get_random_user_agent, urlJoin, get_netloc, min_distance
from gne import GeneralNewsExtractor


def match_digital(data):
    digital = re.findall(r'(\d+)', data, re.IGNORECASE)
    if digital:
        return int(''.join(digital))
    else:
        return None


def get_novels_content(url, **kwargs):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }

    max_content = ''
    html, real_url, status = get_html_by_requests(headers=headers, url=url, **kwargs)
    netloc = get_netloc(real_url)
    if html:
        if netloc in RULES:
            soup = BeautifulSoup(html, 'html5lib')
            selector = RULES[netloc].content_selector
            if selector.get('id', None):
                content = soup.find_all(id=selector['id'])
            elif selector.get('class', None):
                content = soup.find_all(class_=selector['class'])
            else:
                content = soup.find_all(selector.get('tag'))
            if content:
                max_content = content[0].get_text()
        else:
            extractor = GeneralNewsExtractor()
            result = extractor.extract(html, with_body_html=True)
            max_content = result.get('content', '')
            for key in CONTENT_REPLACE:
                max_content = max_content.replace(key, CONTENT_REPLACE[key])
    return '\n'.join([i.strip() for i in max_content.split('\n') if i.strip()]), status


def get_novels_chapter(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': url
    }
    html, real_url, _ = get_html_by_requests(url=url, headers=headers, random_sleep=0)
    netloc = get_netloc(real_url)
    data = dict()
    if html:
        try:
            soup = BeautifulSoup(html, 'html5lib')
        except Exception as e:
            return data
        content_list = []
        if netloc in RULES:
            selector = RULES[netloc].chapter_selector
            if selector.get('id', None):
                content = soup.find_all(id=selector['id'])
            elif selector.get('class', None):
                content = soup.find_all(class_=selector['class'])
            else:
                content = soup.find_all(selector.get('tag'))
            if content:
                for content_item in content:
                    for tag in CHAPTER_TAG:
                        find_tag = content_item.find_all(tag)
                        if find_tag:
                            content_list.extend(find_tag)
        else:
            for tag in CHAPTER_TAG:
                find_tag = soup.find_all(tag)
                if find_tag:
                    content_list.extend(find_tag)

        if content_list:
            story_list = []
            for detail_info in content_list:
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
            all_chapters = []
            for index, item in enumerate(processed_url_list):
                if min_distance(item, max_url) < 2 and len(item.split('/')) == len_max_url:
                    each_data = dict()
                    content_name, content_url = story_list[index]
                    each_data['content_url'] = content_url
                    each_data['content_name'] = content_name
                    index = match_digital(urlparse(content_url).path.split('.')[0].split('/')[-1])
                    if not index:
                        continue
                    each_data['index'] = int(re.findall(r'(\d+)', urlparse(content_url).path.split('.')[0].split('/')[-1])[0])
                    all_chapters.append(each_data)
            chapters_sorted = sorted(all_chapters, reverse=False, key=itemgetter('index'))
            for item in chapters_sorted:
                content_name = item.get('content_name')
                content_url = item.get('content_url')
                res_list.append((content_name, content_url))

            if len(res_list) > 30:
                data['latest_chapter_name'] = res_list[-1][0]
                data['result'] = res_list
                data['netloc'] = get_netloc(real_url)
    return data


if __name__ == '__main__':
    url = 'https://www.dingdiann.com/ddk159053/8312806.html'
    res = get_novels_content(url)
    print(res)

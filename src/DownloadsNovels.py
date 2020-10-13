#!/usr/bin/env python
import os
import re
from operator import itemgetter
from config import RULES, REPLACE_RULES, ENGINE_PRIORITY
from fetcher.cache import get_novels_chapter,get_novels_content
from fetcher.function import get_netloc
from fetcher.novels_tools import get_novels_info


def chapter(url):
    """
    返回小说章节目录页
    """
    netloc = get_netloc(url)
    if netloc not in RULES.keys():
        return None
    if netloc in REPLACE_RULES.keys():
        url = url.replace(REPLACE_RULES[netloc]['old'], REPLACE_RULES[netloc]['new'])
    content = get_novels_chapter(url=url, netloc=netloc)
    if content:
        return content
    else:
        print('解析失败，请将失败页面反馈给本站，请重新刷新一次，或者访问源网页：{url}'.format(url=url))
        return None


def get_content(url=None):
    """
    返回小说章节内容页
    """
    # 当小说内容url不在解析规则内 跳转到原本url
    netloc = get_netloc(url)
    if netloc not in RULES.keys():
        return None
    # 拼接小说目录url
    content_data = get_novels_content(url=url, netloc=netloc)
    return content_data.get('content', '获取失败')


def get_search(name):
    import time
    start = time.time()
    novels_keyword = name.split(' ')[0]
    if not name:
        return None
    # 通过搜索引擎获取检索结果
    parse_result = []

    for each_engine in ENGINE_PRIORITY:
        novels_name = "{name} 小说 阅读 最新章节".format(name=name)
        search_res = get_novels_info(class_name=each_engine, novels_name=novels_name)
        print('{}搜索引擎检索到 {} 个源。'.format(each_engine, len(search_res)))
        parse_result.extend(search_res)

    parse_result = list(filter(None, parse_result))
    if parse_result:
        result_sorted = sorted(
            parse_result,
            reverse=True,
            key=itemgetter('is_recommend', 'is_parse'))
        res_map ={
            'name' :novels_keyword,
            'time' : '%.2f' % (time.time() - start),
            'result': result_sorted,
            'count': len(parse_result)}
        return res_map

    else:
        print("No Result！请将小说名反馈给本站，谢谢！")
        return {}

if __name__ == '__main__':
    limit = 2
    name = '末日后全人类成为了经验值'
    ouput_path = '../result/'
    res = get_search(name)
    print('*'*20 + '检索到全部源' + '*'*20)
    for i in res.get('result', {}):
        print(i)
    is_parse_url = list(set([(i.get('netloc'), i.get('url'), i.get('latest_chapter_name')) for i in res.get('result', {}) if i.get('is_parse')]))
    if is_parse_url:
        is_parse_index = 0
        print('*' * 20 + '已解析源列表' + '*' * 20)
        for i in is_parse_url:
            print("{}. {} . 最新章节 {}".format(is_parse_index, i, i[2]))
            is_parse_index += 1
        input_no = input("输入想要下载编号：")
        input_list = re.split('[ ,、]', input_no)
        for i in input_list:
            netloc, url, latest_chapter_name = is_parse_url[int(i)]
            with open(os.path.join(ouput_path, '{}({}).txt'.format(name, netloc)), 'w+', encoding='utf8') as wf:
                chapter_res = chapter(url)
                if chapter_res:
                    chapter_data = chapter_res.get('result', {})
                    for k in chapter_data:
                        chapter_title, detail_url = chapter_data.get(k)
                        print('获取: {}\n'.format(chapter_title.strip()),end='', flush=True)
                        detail_content = get_content(detail_url)
                        wf.write('{}\n'.format(chapter_title))
                        wf.write('{}\n'.format(detail_content.strip()))


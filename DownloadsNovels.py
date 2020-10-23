#!/usr/bin/env python
import os
import re
from config import REPLACE_RULES, ENGINE_PRIORITY
from fetcher.extract_novels import get_novels_chapter, get_novels_content
from fetcher.novels_tools import get_novels_info
from fetcher.novels_factory import bing_novels, baidu_novels, so_novels
from fetcher.function import check_path_exists


def chapter(url, netloc):
    """
    返回小说章节目录页
    """
    if netloc in REPLACE_RULES.keys():
        url = url.replace(REPLACE_RULES[netloc]['old'], REPLACE_RULES[netloc]['new'])
    content = get_novels_chapter(url=url)
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
    # 拼接小说目录url
    content_data = get_novels_content(url=url)
    return content_data.get('content', '获取失败')


def get_search(name, search_type='all'):
    import time
    start = time.time()
    novels_keyword = name.strip().split(' ')[0]
    if not name:
        return None
    # 通过搜索引擎获取检索结果
    parse_result = []

    if search_type == 'baidu':
        novels_name = "{name} 小说 最新章节".format(name=name)

        search_res = baidu_novels.start(novels_name)
        print('{}搜索引擎检索到 {} 个源。'.format('baidu', len(search_res)))
        parse_result.extend(search_res)

    elif search_type == 'bing':
        novels_name = "{name} 小说 最新章节".format(name=name)
        search_res = bing_novels.start(novels_name)
        print('{}搜索引擎检索到 {} 个源。'.format('bing', len(search_res)))
        parse_result.extend(search_res)

    elif search_type == 'so':
        novels_name = "{name} 小说 最新章节".format(name=name)
        search_res = so_novels.start(novels_name)
        print('{}搜索引擎检索到 {} 个源。'.format('so', len(search_res)))
        parse_result.extend(search_res)
    else:
        for each_engine in ENGINE_PRIORITY:
            novels_name = "{name} 小说 阅读 最新章节".format(name=name)
            search_res = get_novels_info(class_name=each_engine, novels_name=novels_name)
            print('{}搜索引擎检索到 {} 个源。'.format(each_engine, len(search_res)))
            parse_result.extend(search_res)
    parse_result = list(filter(None, parse_result))
    if parse_result:
        res_map = {
            'name': novels_keyword,
            'time': '%.2f' % (time.time() - start),
            'result': parse_result,
            'count': len(parse_result)}
        return res_map

    else:
        print("No Result！请将小说名反馈给本站，谢谢！")
        return {
            'name': novels_keyword,
            'time': '%.2f' % (time.time() - start),
            'count': 0,
            'result': None
        }


def get_parse_novel_source(source_list: list):
    if not source_list:
        return None
    for source in source_list:
        novel_chapters = get_novels_chapter(source.get('url'))
        if novel_chapters:
            novel_chapters['title'] = source.get('title', '未知')
            novel_chapters['source'] = source.get('source', '未知')
            yield novel_chapters


if __name__ == '__main__':
    limit = 2
    name = input("输入想要下载小说名：")
    ouput_path = os.path.join(os.getcwd(), 'result/')
    check_path_exists(ouput_path)
    res = get_search(name, 'all')
    print('耗时：{}s'.format(res.get('time')))
    print('*' * 20 + '开始解析' + '*' * 20)
    result = res.get('result', {})
    parse_novel_source_res_list = []
    if result:
        parse_novel_source_res = get_parse_novel_source(result)
        is_parse_index = 0
        for i in parse_novel_source_res:
            print("{}. 搜索名：{}({})\t章节总数：{}章\t最新章节：{}\t前十章节目录：\n\t{}".format(
                is_parse_index,
                i.get('title', '未知'),
                i.get('netloc', '未知'),
                len(i.get('result', [])),
                i.get('latest_chapter_name', '未知'),
                '|'.join([x[0] for x in i.get('result', [])[:10] if i.get('result', [])])
            ))
            is_parse_index += 1
            parse_novel_source_res_list.append(i)
    if parse_novel_source_res_list:
        input_no = input("输入想要下载编号：")
        input_list = re.split('[ ,、]', input_no)
        for i in input_list:
            netloc = parse_novel_source_res_list[int(i)].get('netloc', '未知')
            latest_chapter_name = parse_novel_source_res_list[int(i)].get('latest_chapter_name', '未知')
            title = parse_novel_source_res_list[int(i)].get('title', '未知')
            chapter_res = parse_novel_source_res_list[int(i)].get('result', [])
            saved_path = os.path.join(ouput_path, '{}({}).txt'.format(name, netloc))
            if chapter_res:
                with open(saved_path, 'w+', encoding='utf8') as wf:
                    print("总章节为 {}".format(len(chapter_res)))
                    input_chapter = input("输入想要下载章节的起始数：")
                    rec = 0
                    for chapter_title, detail_url in chapter_res:
                        if rec < int(input_chapter):
                            rec += 1
                            continue
                        print('获取: {}\n'.format(chapter_title.strip()), end='', flush=True)
                        detail_content = get_content(detail_url)
                        if not detail_content:
                            continue
                        wf.write('{}\n'.format(chapter_title))
                        wf.write('{}\n'.format(detail_content.strip()))
            else:
                print("解析章节目录为空！")
            print("成功下载小说【{}】，存储路径为：{}".format(name, saved_path))

    else:
        print("无解析网站")

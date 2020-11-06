#!/usr/bin/env python
import os
import re
import time
import requests
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor


from config import REPLACE_RULES, ENGINE_PRIORITY
from src.extract_novels import get_novels_chapter, get_novels_content
from src.novels_factory import bing_novels, baidu_novels, so_novels
from src.function import check_path_exists, get_novels_info
from utils.spider_utils import GetFreeProxy


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
        print('{} 检索到 {} 个源。'.format('baidu', len(search_res)))
        parse_result.extend(search_res)

    elif search_type == 'bing':
        novels_name = "{name} 小说 最新章节".format(name=name)
        search_res = bing_novels.start(novels_name)
        print('{} 检索到 {} 个源。'.format('bing', len(search_res)))
        parse_result.extend(search_res)

    elif search_type == 'so':
        novels_name = "{name} 小说 最新章节".format(name=name)
        search_res = so_novels.start(novels_name)
        print('{}检索到 {} 个源。'.format('so', len(search_res)))
        parse_result.extend(search_res)
    else:
        for each_engine in ENGINE_PRIORITY:
            novels_name = "{name} 小说 阅读 最新章节".format(name=name)
            search_res = get_novels_info(class_name=each_engine, novels_name=novels_name)
            print('{} 检索到 {} 个源。'.format(each_engine, len(search_res)))
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


class DownLoadStory:
    def __init__(self, is_proxy=False, ThreadNum=1):
        self.is_proxy = is_proxy
        self.download_status = 1
        self.GFP = GetFreeProxy()
        self.proxy_ip = PriorityQueue(maxsize=5000)
        self.close_proxy_ip = []
        self.proxy_update_time_record = time.time()
        self.proxy_update_time_frequency = 30
        self.temp_story = {}
        if is_proxy:
            ThreadNum += 1
        self.executor = ThreadPoolExecutor(max_workers=ThreadNum)
        self.kanban = {
            'download_done': 0,
            'all_chapter_num': 1
        }

    def save_close_ip(self, ip):
        diff_len_queue = 5000 - len(self.close_proxy_ip)
        if diff_len_queue > 0:
            del self.close_proxy_ip[0: diff_len_queue]
        if ip not in self.close_proxy_ip:
            self.close_proxy_ip.append(ip)

    def update_proxy_ip(self):
        while self.download_status:
            time_fre = time.time() - self.proxy_update_time_record
            if not self.proxy_ip.empty() and time_fre < self.proxy_update_time_frequency:
                time.sleep(int(self.proxy_update_time_frequency - time_fre))
            self.proxy_update_time_record = time.time()
            level = 999
            response = requests.get('https://ip.jiangxianli.com/api/proxy_ips', timeout=5)
            if response.status_code == 200:
                for i in response.json().get('data', {}).get('data', []):
                    self.proxy_ip.put((998, '{}:{}'.format(i.get('ip'), i.get('port'))))
            try:
                for i in self.GFP.freeProxyData5u():
                    self.proxy_ip.put((level, i))
            except:
                import traceback
                traceback.print_exc()
                print('{} 代理IP失败！'.format('freeProxyData5u'))

            try:
                for i in self.GFP.freeProxyGouBanJia():
                    self.proxy_ip.put((level, i))
            except:
                print('{} 代理IP失败！'.format('freeProxyGouBanJia'))

            try:
                for i in self.GFP.freeProxyIp3366():
                    self.proxy_ip.put((level, i))
            except:
                print('{} 代理IP失败！'.format('freeProxyIp3366'))

            try:
                for i in self.GFP.freeProxyJiangXianLi():
                    self.proxy_ip.put((level, i))
            except:
                print('{} 代理IP失败！'.format('freeProxyJiangXianLi'))

            try:
                for i in self.GFP.freeProxyKuaiDaiLi():
                    self.proxy_ip.put((level, i))
            except:
                print('{} 代理IP失败！'.format('freeProxyKuaiDaiLi'))

            try:
                for i in self.GFP.freeProxyWallProxyListPlus():
                    self.proxy_ip.put((level, i))
            except:
                print('{} 代理IP失败！'.format('freeProxyWallProxyListPlus'))

    def start_update_proxy(self):
        self.executor.submit(self.update_proxy_ip)

    def get_open_ip(self):
        while 1:
            level, proxy_ip = self.proxy_ip.get()
            if proxy_ip not in self.close_proxy_ip:
                return proxy_ip

    def download_story(self, url, retry=5):
        while retry > 0:
            if self.is_proxy:
                proxy_ip = self.get_open_ip()
                proxies = {
                    'http': 'http://{}'.format(proxy_ip),
                    'https': 'http://{}'.format(proxy_ip)
                }

                detail_content, status = get_novels_content(url=url, proxies=proxies)
                if not detail_content and not status:
                    retry -= 1
                    self.save_close_ip(proxy_ip)
                elif status == 200 or status == 302:
                    self.proxy_ip.put((998, proxy_ip))
                    self.kanban['download_done'] += 1
                    print('下载完成度：{}'.format(self.kanban['download_done'] / self.kanban['all_chapter_num']))
                    return detail_content
                else:
                    print("下载失败：{}【{}】".format(url, status))
                    return ''
            else:
                detail_content, status = get_novels_content(url=url)

                if not detail_content and not status:
                    retry -= 1
                    print('正在重试：{}'.format(url))
                elif status == 200 or status == 302:
                    self.kanban['download_done'] += 1
                    print('下载完成度：{}'.format(self.kanban['download_done'] / self.kanban['all_chapter_num']))
                    return detail_content
                else:
                    print("下载失败：{}【{}】".format(url, status))
                    return ''

        return ''

    def multi_thread_download(self, chapter_res):
        if self.is_proxy:
            self.executor.submit(self.update_proxy_ip)
        task_rec = []
        self.kanban['all_chapter_num'] = len(chapter_res)
        for _, url in chapter_res:
            print('提交下载任务：{}'.format(url))
            task_rec.append(self.executor.submit(self.download_story, (url)))
        rec = 0
        while self.download_status:
            time.sleep(10)
            if all([task.done() for task in task_rec]):
                self.download_status = 0
            rec += 1
        res = [task.result() for task in task_rec]
        return res

    def run(self):
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
                print("【{}】. 搜索名：{}({})\t章节总数：{}章\t最新章节：{}\t前十章节目录：\n\t{}".format(
                    is_parse_index,
                    i.get('title', '未知'),
                    i.get('netloc', '未知'),
                    len(i.get('result', [])),
                    i.get('latest_chapter_name', '未知'),
                    '|'.join([x[0] for x in i.get('result', [])[:10] if i.get('result', [])])
                ))
                print('*' * 100)
                is_parse_index += 1
                parse_novel_source_res_list.append(i)
        if parse_novel_source_res_list:
            input_no = input("输入想要下载编号：")
            input_list = re.split('[ ,、]', input_no)
            for i in input_list:
                netloc = parse_novel_source_res_list[int(i)].get('netloc', '未知')
                chapter_res = parse_novel_source_res_list[int(i)].get('result', [])
                saved_path = os.path.join(ouput_path, '{}({}).txt'.format(name, netloc))
                if chapter_res:
                    print("总章节为 {}".format(len(chapter_res)))
                    input_chapter = input("输入想要下载章节的起始数：")

                    with open(saved_path, 'w+', encoding='utf8') as wf:
                        rec = 0
                        for chapter_title, detail_url in chapter_res:
                            if rec < int(input_chapter):
                                rec += 1
                                continue
                            detail_content, status = get_novels_content(url=detail_url)
                            print("获取 {} {}".format(chapter_title, status))
                            if not detail_content:
                                continue
                            wf.write('{}\n'.format(chapter_title))
                            wf.write('{}\n'.format(detail_content.strip()))
                else:
                    print("解析章节目录为空！")
                print("成功下载小说【{}】，存储路径为：{}".format(name, saved_path))

        else:
            print("无解析网站")

    def run_mult_thread(self, ):
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
                print("【{}】. 搜索名：{}({})\n\t章节总数：{}章\n\t最新章节：{}\n\t前十章节目录：\n\t{}".format(
                    is_parse_index,
                    i.get('title', '未知'),
                    i.get('netloc', '未知'),
                    len(i.get('result', [])),
                    i.get('latest_chapter_name', '未知'),
                    '|'.join([x[0] for x in i.get('result', [])[:10] if i.get('result', [])])
                ))
                print('*' * 100)
                is_parse_index += 1
                parse_novel_source_res_list.append(i)
        if parse_novel_source_res_list:
            input_no = input("输入想要下载编号：")
            input_list = re.split('[ ,、]', input_no)
            for i in input_list:
                netloc = parse_novel_source_res_list[int(i)].get('netloc', '未知')
                chapter_res = parse_novel_source_res_list[int(i)].get('result', [])
                saved_path = os.path.join(ouput_path, '{}({}).txt'.format(name, netloc))
                if chapter_res:
                    print("总章节为 {}".format(len(chapter_res)))
                    input_chapter = input("输入想要下载章节的起始数：")
                    story_contents = self.multi_thread_download(chapter_res[int(input_chapter):])
                    with open(saved_path, 'w+', encoding='utf8') as wf:
                        wf.write('{}\n'.format('\n'.join(story_contents)))
                    print("成功下载小说【{}】，存储路径为：{}".format(name, saved_path))
                else:
                    print("解析章节目录为空！")


        else:
            print("无解析网站")


if __name__ == '__main__':
    DLS = DownLoadStory()
    DLS.run_mult_thread()

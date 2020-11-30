#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
import time

from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor
from story_dl.extract_novels import get_novels_content, get_netloc
import requests
import re

from utils.spider_utils import GetFreeProxy
from story_dl.downloadStoryMain import get_search, get_parse_novel_source
from story_dl.rules import RULES


class getSearchResultThread(QThread):
    result_dict_signal = pyqtSignal(dict)

    def __init__(self, search_name, search_type):
        super(getSearchResultThread, self).__init__()
        self.search_name = search_name
        self.search_type = search_type

    def run(self) -> None:
        res = get_search(self.search_name, self.search_type)
        result = res.get('result', {})
        single_dict = dict()
        single_dict['error_message'] = None
        single_dict['search_stats'] = -1
        if not result:
            single_dict['error_message'] = '没有检索到结果！'
            self.result_dict_signal.emit(single_dict)
        else:
            parse_novel_source_res = get_parse_novel_source(result)
            row = res.get('count', 0)
            is_parse_index = 0
            for i in parse_novel_source_res:
                if i.get('netloc', '未知') in RULES:
                    i['is_parse'] = 1
                else:
                    i['is_parse'] = 0
                i['is_parse_index'] = is_parse_index
                i['row'] = row
                i['search_stats'] = 1
                is_parse_index += 1
                self.result_dict_signal.emit(i)
            single_dict['search_stats'] = 0
            self.result_dict_signal.emit(single_dict)


class downloadStoryHandler(QThread):
    result_dict_signal = pyqtSignal(dict)

    def __init__(self, download_story_list, is_proxy, thread_num):
        super(downloadStoryHandler, self).__init__()
        self.download_story_list = download_story_list
        self.download_status = True
        self.is_proxy = is_proxy
        self.thread_num = thread_num
        self.GFP = GetFreeProxy()
        self.proxy_ip = PriorityQueue(maxsize=5000)
        self.close_proxy_ip = []
        self.proxy_update_time_record = time.time()
        self.proxy_update_time_frequency = 30
        self.temp_story = {}
        self.kanban = {
            'download_done': 0,
            'all_chapter_num': 1
        }
        self.executor = ThreadPoolExecutor(max_workers=self.thread_num)
        self.result_dict_signal.emit({'status': 0})
        if is_proxy:
            self.thread_num += 1
            self.start_update_proxy()

    def save_close_ip(self, ip):
        diff_len_queue = 5000 - len(self.close_proxy_ip)
        if diff_len_queue > 0:
            del self.close_proxy_ip[0: diff_len_queue]
        if ip not in self.close_proxy_ip:
            self.close_proxy_ip.append(ip)

    def update_proxy_ip(self):
        print('代理池启动！')
        while self.download_status:
            time_fre = time.time() - self.proxy_update_time_record
            if time_fre < self.proxy_update_time_frequency:
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

    def download_story(self, url, retry=50):
        while retry > 0 and self.download_status:
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
                    self.result_dict_signal.emit(
                        {'status': self.kanban['download_done'] / self.kanban['all_chapter_num']})
                    print("下载成功：{}【{}】".format(url, status))
                    return detail_content
                else:
                    print("下载失败：{}【{}】".format(url, status))
                    return ''
            else:
                detail_content, status = get_novels_content(url=url)

                if not detail_content and not status:
                    retry -= 1
                    print('正在重试：{} 【{}】'.format(url, status))
                elif status == 200 or status == 302:
                    self.kanban['download_done'] += 1
                    self.result_dict_signal.emit(
                        {'status': self.kanban['download_done'] / self.kanban['all_chapter_num']})
                    print("下载成功：{}【{}】".format(url, status))
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
        for name, url in chapter_res:
            task_rec.append((name, self.executor.submit(self.download_story, (url))))
        print('提交下载任务完成')
        while self.download_status:
            time.sleep(10)
            if all([task.done() for _, task in task_rec]):
                self.download_status = False
        res = []
        for name, task in task_rec:
            task_res = task.result()
            res.append(re.sub(r'(章节|章|回|卷|\.)', '\g<1> ', name) + '\n' + task_res)
        return res

    def start_download_story(self):
        print('开始下载')
        for story_chapter_list, saved_path in self.download_story_list:
            with open(saved_path, 'w+', encoding='utf8') as wf:
                for chapter_title, detail_url in story_chapter_list:
                    detail_content, status = get_novels_content(url=detail_url)
                    print("获取 {} {}".format(chapter_title, status))
                    if not detail_content:
                        continue
                    wf.write('{}\n'.format(re.sub(r'(章节|章|回|卷|\.)', '\g<1> ', chapter_title)))
                    wf.write('{}\n'.format(detail_content))
            print("成功下载小说:{}".format(saved_path))

    def start_download_story_multithread(self):
        print('开始下载')
        for story_chapter_list, saved_path in self.download_story_list:
            story_contents = self.multi_thread_download(story_chapter_list)
            with open(saved_path, 'w+', encoding='utf8') as wf:
                wf.write('{}\n'.format('\n'.join(story_contents)))
            print("成功下载小说:{}".format(saved_path))

    def run(self) -> None:
        try:
            if self.thread_num > 1:
                self.start_download_story_multithread()
            else:
                self.start_download_story()
        except Exception as e:
            import traceback
            traceback.print_exc()

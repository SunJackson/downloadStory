#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

from importlib import import_module


def get_novels_info(class_name, novels_name):
    novels_module = import_module(
        "fetcher.{}.{}_novels".format('novels_factory', class_name))
    # 获取对应渠道实例化对象

    novels_info = novels_module.start(novels_name)
    return novels_info

if __name__ == '__main__':
    print(get_novels_info('', '盗墓笔记'))
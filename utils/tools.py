#!/usr/bin/env python
import asyncio

from functools import wraps


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance


r'(第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集]\s*.*?)[_,-]'
common_used_numerals_tmp = {'零': 0,
                            '一': 1,
                            '二': 2,
                            '两': 2,
                            '三': 3,
                            '四': 4,
                            '五': 5,
                            '六': 6,
                            '七': 7,
                            '八': 8,
                            '九': 9,
                            '十': 10,
                            '〇': 0,
                            '壹': 1,
                            '贰': 2,
                            '叁': 3,
                            '肆': 4,
                            '伍': 5,
                            '陆': 6,
                            '柒': 7,
                            '捌': 8,
                            '玖': 9,
                            '拾': 10,
                            '百': 100,
                            '千': 1000,
                            '貮': 2,
                            '俩': 2,
                            '１': 1,
                            '２': 2,
                            '３': 3,
                            '４': 4,
                            '５': 5,
                            '６': 6,
                            '７': 7,
                            '８': 8,
                            '９': 9,
                            '０': 0,
                            '佰': 100,
                            '仟': 1000,
                            '萬': 10000,
                            '万': 10000,
                            '亿': 100000000,
                            '億': 100000000,
                            '兆': 1000000000000}

common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十',
                        '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '貮', '俩', ]
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿',
                       '〇', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '貮', '俩', '佰', '仟', '萬', '億', '兆']


def ChineseNumToArab(oriStr):
    lenStr = len(oriStr)
    aProStr = ''
    if lenStr == 0:
        return aProStr
    hasNumStart = False
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True
            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False
                    aProStr += numResult
            aProStr += oriStr[idx]
            pass
    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)
    return aProStr

if __name__ == '__main__':
    print(ChineseNumToArab('第一千三百五十章'))
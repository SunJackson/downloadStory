#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:SunJackson
# @datetime:2020/11/21 15:28
# @file: handerMysql.py
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setting import ENGINE
# from rules import RULES
# from datetime import datetime

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DownloadRules(Base):
    '''
CREATE TABLE `download_rules` (
  `domain` text NOT NULL,
  `chapter_selector` text,
  `content_selector` text,
  `chapter_url_format` text,
  `content_url_format` text,
  `is_ok` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

    '''

    __tablename__ = 'download_rules'
    # 表的结构:
    domain = Column(String(60), index=True, primary_key=True)
    chapter_selector = Column(String(60))
    content_selector = Column(String(60))
    chapter_url_format = Column(String(128))
    content_url_format = Column(String(128))
    is_ok = Column(Integer)
    update_time = Column(Date)
    create_time = Column(Date)




# Base.metadata.create_all(ENGINE)


class HanderMysql:
    def __init__(self):
        # 初始化数据库连接:
        DBSession = sessionmaker(bind=ENGINE)
        self.session = DBSession()

    def insert_download_rules(self, item):
        download_rules = DownloadRules(**item)
        # 添加到session:
        self.session.add(download_rules)
        # 提交即保存到数据库:
        self.session.commit()

    # def upload_rules(self):
    #     for key in RULES:
    #         insert_dict = {
    #             'domain': key,
    #             'chapter_selector': str(RULES[key].chapter_selector),
    #             'content_selector': str(RULES[key].content_selector),
    #             'chapter_url_format': '',
    #             'content_url_format': '',
    #             'is_ok': 1,
    #             'update_time': datetime.now(),
    #             'create_time': datetime.now()
    #         }
    #         self.insert_download_rules(insert_dict)
    #         print('插入数据：{}'.format(insert_dict))

    def download_rules(self):
        download_rules = self.session.query(DownloadRules).filter(DownloadRules.is_ok == 1).all()
        if not download_rules:
            return None
        for i in download_rules:
            yield i

if __name__ == '__main__':
    HM = HanderMysql()
    for i in HM.download_rules():
        print(i.domain)

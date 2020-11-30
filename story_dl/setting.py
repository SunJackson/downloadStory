#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:SunJackson
# @datetime:2020/11/21 14:27
# @file: setting.py
from sqlalchemy import create_engine
ENGINE = create_engine('mysql+pymysql://storyuser:story-dl-123@47.105.129.179:3306/storydl')
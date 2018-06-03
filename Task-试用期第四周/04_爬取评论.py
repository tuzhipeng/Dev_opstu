#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: zhipeng time:2018/6/2

import requests
import bs4
from bs4 import BeautifulSoup


def GetHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def FillList(html):
    ulist = []
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup(class_='floor'):
        comment = str(tr.td).replace(str(tr.blockquote), '').replace(str(tr.small), '')
        ulist.append([comment])

    return ulist


def PrintList(ulist):
    file = open('C://Users//涂志鹏//Desktop//Dev_ops//Task-试用期第四周//Comments.txt', 'w+')
    file.write('\n'.join('%s' % id for id in ulist))
    file.close()


def main():
    url = "https://bbs.hupu.com/20415703.html"
    html = GetHtmlText(url)
    ulist = FillList(html)
    PrintList(ulist)


main()

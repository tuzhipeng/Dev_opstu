#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: zhipeng time: 2018/7/30
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
from updateListen import checkUpdate
import time
import json
from bson import json_util
from flask import jsonify


login_url = "http://221.233.24.23/eams/login.action"
info_url = "http://221.233.24.23/eams/stdDetail.action"
grade_url = "http://221.233.24.23/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"

client = MongoClient("localhost", 27017)
db = client["grade_system"]
col = db["DATA"]


def getInfos(user_id, passwd,sleep_time=2):
    driver = webdriver.PhantomJS()
    driver.get(login_url)
    
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submitBtn")
    #通过JS的ID属性找到“用户名”，“密码” ， “登录”的输入框，并分别命名

    username.send_keys(user_id)
    password.send_keys(passwd)
    time.sleep(sleep_time)
    submit.click()
    #通过send_keys将传入函数的参数导入输入框并提交，实现登录
    ####################开始爬个人信息################
<<<<<<< HEAD
    try:
        driver.get(info_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        infos = {}
        info = {}
        trs = soup.find_all('tr')
        infos['状态'] = '正常'
        if "密码错误" in html:
            infos['状态'] = '密码错误'
            return ""
        if "账户不存在" in html:
            infos['状态'] = '账户不存在'
            return ""
=======
    driver.get(info_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    infos = {}
    info = {}
    trs = soup.find_all('tr')
    infos['状态'] = '正常'
    if "密码错误" in html:
        infos['状态'] = '密码错误'
        return ""
    if "账户不存在" in html:
        infos['状态'] = '账户不存在'
        return ""
>>>>>>> 6e4d0bda84f6e797079f3e6dc4bcf9cd6123e6de

        for tr in trs[1:-1]:
            tds = tr.find_all('td')
            if len(tds) < 2:
                continue
            info[tds[0].getText()[:-1]] = tds[1].getText()
            info[tds[2].getText()[:-1]] = tds[3].getText()

        ########基本信息爬取完毕，开始爬取绩点###########
        driver.get(grade_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        point_keys = []
        points = []

        all_points = {}
        tables = soup.findAll('table')
        point_trs = tables[0].findAll('tr')
        #找到trs，再开始从trs里找th，td
        point_ths = point_trs[0].findAll('th')
        for point_th in point_ths:
            point_keys.append(point_th.getText())

        for point_tr in point_trs[1:-2]:
            point_tds = point_tr.findAll('td')
            for idx, point_td in enumerate(point_tds):
                all_points[point_keys[idx]] = point_td.getText()
            points.append(all_points)
            all_points = {}


        #开始爬取在校汇总绩点
        all_point_ths = point_trs[-2].findAll('th')
        sum_point = {}
        all_point_keys = ["种类","必修门数","必修总学分","必修平均绩点"]
        for idx, all_point_th in enumerate(all_point_ths):
            sum_point[all_point_keys[idx]] = all_point_th.getText()
        points.append(sum_point)
        
        #开始爬取全部成绩
        grades = []
        all_grades = {}
        all_grade_keys = []
        all_grade_trs = tables[1].findAll("tr")
        all_grade_ths = all_grade_trs[0].findAll('th')
        for all_grade_th in all_grade_ths:
            all_grade_keys.append(all_grade_th.getText())
        for all_grade_tr in all_grade_trs:
            all_grade_tds = all_grade_tr.findAll('td')
            for idx, all_grade_td in enumerate(all_grade_tds):
                all_grades[all_grade_keys[idx]] = all_grade_td.getText().strip()
            grades.append(all_grades)
            all_grades = {}
        print("success!!!")

        #把个人信息，绩点，成绩，全部都添加到一个大的字典里去

        
        infos["个人信息"] = info
        infos["绩点"] = points
        infos["成绩"] = grades
        infos["user_id"] = user_id
        infos["passwd"] = passwd
        infos["更新时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        infos["时间戳"] = time.time()
        return infos
    except:
        return ""


def GetInfos(user_id, passwd):
    infos = col.find({"user_id": user_id})
    if infos.count() == 1:
        if infos[0]["passwd"] == passwd:
            if time.time() - int(infos[0]["时间戳"]) < 3600*5:
                return infos[0] 
            else:
                infos = getInfos(user_id, passwd)
                while infos["状态"] != "正常":
                    infos = getInfos(user_id, passwd)
                infos["sign"] = ""
                col.update({"user_id": user_id}, infos)
                return infos
        else:
            return ""
            
    elif infos.count() == 0:
        infos = getInfos(user_id, passwd)
        if infos:
            infos["sign"] = "first"
            col.insert(infos)
            return infos
        else:
            return ""
<<<<<<< HEAD


=======
>>>>>>> 6e4d0bda84f6e797079f3e6dc4bcf9cd6123e6de
def mailUpdate(user_id, email):
    col.update({"user_id": user_id},{"$set":{"订阅":email}})








#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: zhipeng time: 2018/7/30
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g
from GetGrades import getInfos, GetInfos, mailUpdate
from updateListen import checkUpdate
import json
import time
from bson import json_util
import os


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']=os.urandom(24)


@app.route('/', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/info', methods=["POST", "GET"])

def info():
    if request.method == "GET":
        return redirect(url_for('login'))
    else:
        
        user_id  = request.form.get("user_id")
        password = request.form.get("password")
        infos = GetInfos(user_id, password) 
        
        if infos:
            session['user_id'] = user_id
            return render_template('info.html', content=infos)
        else:
            return render_template('alert_html/login.html')

@app.route('/email', methods=["POST", "GET"])

def email():
    if request.method == "GET":
        if session.get('user_id'):
            return render_template("email.html")
        else:
            return redirect(url_for('login'))
    else:
        email = request.form.get("email")
        user_id = session.get('user_id')
        if email:
            session['email'] = email
            mailUpdate(user_id, email)
            checkUpdate()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('email'))
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)



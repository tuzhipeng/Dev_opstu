# 暑假作业
---
主要分3个部分：

 1. Flask主要框架
 2. 爬虫程序
 3. 监听及发邮件程序
 
---




## 目录
---
- [app.py][1]：Flask主要框架文件
- [GetGrades.py][2]：Python爬虫主文件，获取主要信息并插入到数据库中
- [updateListen.py][3]：监听成绩是否有更新，若有，则发送邮件
- [static/css][4]：界面的样式文件
- [templates/login.html][5]：登录页面
- [templates/info.html][6]：成绩页面
- [templates/email.html][7]：填写邮箱页面

---
## 详细介绍
---
### app.py ：分3个路由

> / 基础登录页面 

> /info 爬取成绩后的页面展现

> /email 填写邮件的页面


### GetGrades.py：分3个函数

> **getInfos函数**

直接从教务处上爬取信息，采用的是selenium+phantomJS实现爬取，存储的数据结构是：

```
{
    "个人信息" : {}
    "绩点" : [{},{},{}]
    "成绩" : [{},{},{}...]
    "user_id" : ""
    "passwd": ""
    .........
}
```
> **GetInfos函数**

当用户访问 **/info**页面时 判断数据库中是否有用户的信息，如果有那么直接从数据库中提取，如果没有，那么调用getInfos函数来爬取数据，并添加`first`标记（也就是在字典中添加`"sign" : "first"`这个键值对，以便给用户在第一次填写完邮箱之后立即给用户发一封邮件），最后插入到数据库中

> **mailUpdate函数**

当用户点击填写邮箱并提交时，则会到该用户的数据中插入`"订阅":" *用户填写的email* "` 以此来为用户添加标记

### UpdateListen.py：分3个函数

> **sendemail函数**

此处使用的是163邮箱的smtp协议来发送邮件，首先要去163邮箱里去开通SMTP服务，再开启授权码,至于函数怎么写可以参考 **[菜鸟教程Python SMTP][8]** 
方法如下图 :

![SMTP](https://images.gitee.com/uploads/images/2018/0807/110643_9d426de9_2046054.png "smtp.png")

![授权码](https://images.gitee.com/uploads/images/2018/0807/121738_58a94960_2046054.png "授权码.png")，

> **checkUpdate函数**

遍历数据库中所有带有订阅标记的用户，调用GetGrades.py中的`getInfos`函数抓取当前的信息记为 `new_info` ，然后比对 `new_info`  中的*“成绩”*与之前数据库中存在的信息中的*“成绩”*，看是否一致，再看之前的信息中是否存在`first`标记，如果满足二者条件之一，就开始构建HTML表格内容作为`content`，将`content`作为参数传入`sendmail`函数，再调用`sendmail`函数发出邮件，最后把新数据插入到数据库，注意！，新数据中没有订阅标记，还要调用GetGrades.py中的`mailUpdate`函数为用户添加订阅标记，以便下一次成绩更新后能正常发出邮件

> **listen函数**

一个监听函数，实现每5个小时调用一次checkUpdate函数

---
## 附
---
- app.py和updateListen.py这两个程序要一直处于运行状态，我们把它放到后台运行

`nohup python3 app.py `

`nohup python3 updateListen.py`

- 如果想关闭这两个后台程序

` ps -aux` 查看所有的后台程序，每个进程都有一个PID

` kill -9 PID号 ` 这个-9表示强行关闭，可以不加

---
## 完成图
---
![login](https://images.gitee.com/uploads/images/2018/0807/125143_971416e3_2046054.png "登录.png")
![info](https://images.gitee.com/uploads/images/2018/0807/125120_d8551f9d_2046054.png "info.png")
![email](https://images.gitee.com/uploads/images/2018/0807/125206_1483d11b_2046054.png "mail.png")

---
## 遇到的困难
---
- Debian9 安装mailx的时候提醒有两个版本，结果我两个版本都安装试过了，都不能发邮件，只能换成 Centos7 （ *现已解决* ）我百度了下该怎么发邮件，都说要装mailx，所以在测试发邮件的时候一直都是测用mailx发，不是用SMTP协议，结果Debian一直发不出去，结果就换centos了，没想到代码全部完工后，转到Debian上能正常发邮件，唉，/ :joy: 
- 很多函数需要`user_id`，`email`，这些参数，但我没能做到让这参数全局可见，用g对象搞了好久没能搞定，最后还是用的session存储这些参数，才搞定，不知道有没有更好的方法
- 跳转到填写邮箱页面没有做登录限制，暂时也没想到该怎么做（ *现已解决* ）还是把代码好好优化了一下，还是把登录限制做了出来，并且一些警告框也做了，可惜的是还是没能做到不及格变红，之后看看JS吧。。。/ 有点可惜 :relieved: 

---
## 得到的帮助
---

- 首先就是 **[苏金鹏的代码][9]** 了，大致的框架都是模仿他的，在他的框架基础上做了一些外观上的提升，还加自己的一些想法 :smirk: 

- 其次就是 **[周淦清的代码][10]** 了，模仿了他的发邮件的函数（差不多是照搬  /笑哭/） :joy: 

---
## 收获
---

 1. 对Flask的认识更深了
 2. 了解了Linux发邮件的一些操作
 3. 对数据库的操作更熟了
 4. 把爬虫自己重新又写了一遍，对爬虫少了很多畏惧感
 5. 对于HTML做成表格的形式有了新的认识


  [1]: app.py
  [2]: GetGrades.py
  [3]: updateListen.py
  [4]: static/css
  [5]: templates/login.html
  [6]: templates/info.html
  [7]: templates/email.html
  [8]: http://www.runoob.com/python3/python3-smtp.html
  [9]: https://github.com/suings/Dev_ops/tree/master/Summer/flask
  [10]: https://gitee.com/Mark-ThinkPad/2018_Summer_Holiday/tree/master/task/%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2%E7%B3%BB%E7%BB%9F
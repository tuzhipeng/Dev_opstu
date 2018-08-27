# Docker入门

---
## 基本用法：

### docker基本操作

docker images

docker ps -a -l （-a表示查看所有的容器，包括未运行的，-l表示看最新操作过的容器）

docker run ubuntu echo hello world

### 交互式容器

docker run --name [自主命名的容器名称]-i -t ubuntu /bin/bash 

进入容器内部 --name 表示将容器自主命名，方便之后通过自己命的名对它操作，-i表示一直可以输入，-t表示

docker inspect [容器名称或者ID号] 查看容器的详细信息

docker start -i [容器名称或ID号] 重新启动已经停止的容器，-i表示一直可以输入

docker rm 删除容器

Ctrl p  + Ctrl q 表示退出容器内部，但不关闭容器，在容器内exit才是关闭容器

docker attach [容器名称或ID号] 重新进入正在运行的容器中

### 守护式容器

docker run -d --name [自主命名的容器名称] ubuntu /bin/bash

创建了一个守护式容器，-d表示后台运行

docker logs -t -f --tail 10 [容器名称或ID号]
查看日志，日志内有容器运行结果，-t表示运行结果前加上时间，-f表示显示当前运行的结果，--tail后面加数字N表示显示最新的N条，N取零表示显示最新的一条

docker top [容器名称或ID号] 查看当前容器的进程

docker stop [容器名称或ID号] 停止运行当前的容器

docker kill [容器名称或ID号] 立即停止运行当前的容器

## 在容器中部署静态网站

 1. docker run -p 8080:80 --name [名称] -i -t ubuntu /bin/bash 创建映射80端口的交互式容器，以下操作均在容器内进行
 
 2. apt-get install -y nginx vim 安装vim和nginx，如果显示docker E: Unable to locate package nginx则需要先apt-get update再安装
 
 3. mkdir -p /usr/www/html 先创建一个目录，在这个目录下放HTML文件，
 
 4. 再用whereis nginx 命令，找到nginx的位置，修改配置文件，vim /etc/nginx/site-enabled/default  进入修改root后面的路径为你创建目录的路径，即root /usr/www/html;
 
 5. 直接在容器内打 nginx 运行nginx服务即可通过浏览器访问你的IP和端口看到你的网页

 
 
---

# 先来一波笔记保命。。。23333

这些笔记都是我看玩视频敲出来的 /笑哭 ，dockerfile的一些用法我也知道，但还是没能完成任务，几乎是照搬苏金鹏的代码，镜像到是做出来了（也不知道对不对），但老是跑不出界面，惭愧的很, 唉，只能等等开学再去请教一哈大佬们了。。。


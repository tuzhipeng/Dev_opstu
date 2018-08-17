import traceback
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pymongo import MongoClient
import GetGrades
import time


client =MongoClient("localhost", 27017)
db = client['grade_system']
col = db['DATA']


def sendmail(email, content):
    
    # 发件人和收件人
    sender = "13986717767@163.com"
    receiver = email
    
    # 所使用的用来发送邮件的SMTP服务器
    smtpserver = "smtp.163.com"
    
    # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
    username = "13986717767@163.com"
    password = "Tuzhipeng00"
    
    # 邮件主题(这个邮件主题应该加个颜文字卖卖萌的)
    mail_title = "成绩更新通知邮件"

    # 安排邮件内容
    mail_body = content

    # 邮件内容, 格式, 编码
    message = MIMEText(mail_body, 'html', 'utf-8')
    message['From'] = sender # 发件人
    message['To'] = receiver # 收件人
    message['Subject'] = Header(mail_title, 'utf-8')

    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com",465)
       
        smtp.login(username, password)
        
        smtp.sendmail(sender, receiver, message.as_string())
        
        smtp.quit()
        print("发送邮件成功")
    except smtplib.SMTPException:
        print("发送邮件失败")


def checkUpdate():
    for info in col.find({"订阅":{"$regex":"[\s\S]*"}}):
        user_id = info["user_id"]
        passwd = info["passwd"]
        email = info["订阅"]
        new_info = GetGrades.getInfos(user_id, passwd)
        
        if info["成绩"] != new_info["成绩"] or info["sign"] == "first":
            info_list = """
			<style type="text/css">
			table{
					text-align: center;
					border-collapse:collapse;
					border: 4px solid;
			}
			td,th{
					border-color: black;
					border: 2px solid;
			}
			</style>
			<table ">

					<tr>
						<th>姓名</th><th>学号</th><th>性别</th><th>学制</th><th>所属班级</th>
					</tr>
    """
            info_base = """
    <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
    """
            
            info_list = info_list + info_base.format(new_info["个人信息"]["姓名"],new_info["个人信息"]["学号"],new_info["个人信息"]["性别"],new_info["个人信息"]["学制"],new_info["个人信息"]["所属班级"])
			#-----------------------------
            point_list ="""
			<tr>
					<th>学年度</th><th>学期</th><th>必修门数</th><th>必修总学分</th><th>必修平均绩点</th>
			</tr>"""
            point_base ="""<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
			"""

            for jd in new_info["绩点"][:-1]:
                point_list = point_list + point_base.format(jd["学年度"],jd["学期"],jd["必修门数"],jd["必修总学分"],jd["必修平均绩点"])
            
            
            point_list = point_list +point_base.format("在校汇总","全",new_info["绩点"][-1]["必修门数"],new_info["绩点"][-1]["必修总学分"],new_info["绩点"][-1]["必修平均绩点"])
			#-----------------------------------
            grade_list="""
						<tr>
					<th>课程名称</th><th>课程时间</th><th>学分</th><th>最终成绩</th><th>绩点</th>
			</tr>"""
            grade_base = """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"""
			
            
            for cj in new_info["成绩"][1:]:
                grade_list = grade_list + grade_base.format(cj["课程名称"],cj["学年学期"],cj["学分"],cj["总评成绩"],cj["绩点"])
            		
            
            content = info_list + point_list + grade_list +"</table>"
           
            sendmail(email,content)
            col.update({"user_id": user_id},new_info)
            GetGrades.mailUpdate(user_id, email)
            col.update({"user_id": user_id},{"$set":{"sign":""}})
            

def listen():
    while 1:
        checkUpdate()
        time.sleep(10)
if __name__ == "__main__":
    listen()

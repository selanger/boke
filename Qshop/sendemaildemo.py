import smtplib
from email.mime.text import MIMEText

## 构建邮件
## 主题
subject = "0715测试damo"
# 发送内容
content = "Good Good study,day day up"
# 发送人
sender = "str_wjp@163.com"
# 接收人  单个  多个收件人
rec = """673898321@qq.com,
2287373840@qq.com,
anjunhui@aliyun.com,
1162347614@qq.com
"""

password = "qaz123"
###  MIMEText 参数 发送内容， 内容类型 , 编码
message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["From"] = sender   ## 发件人
message["To"] = rec   ## 收件人

### 发送邮件
smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
## 参数说明    发件人    收件人需要一个列表     发送邮件 类似一种json的格式
smtp.sendmail(sender,rec.split(",\n"),message.as_string())

smtp.close()




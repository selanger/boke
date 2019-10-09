from __future__ import absolute_import
from Qshop.celery import app
import time
## 创建任务
@app.task      ## 将普通的函数转换为celery任务
def test():
    time.sleep(2)
    print("-----i am test task-----")
    return "i am test task"

@app.task
def myprint(name,age):
    time.sleep(5)
    print("%s:%s"%(name,age))
    return "woshi myprint"

@app.task
def send_email(params):
    ##  发送邮件的代码 发送短信
    ##
    return "send email"

@app.task
def send_code(params):
    """
    :param params:  字典类型     phone  code
    :return:
    """
    ##  发送短信验证码
    import requests
    ## 请求地址
    url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
    # APIID
    account = "C53007282"
    # APIkey
    password = "62aa30a7402d2ffa127b33e7e94e7a0f"
    ## 收件人手机号
    mobile = params.get("phone")
    ## 短信内容
    content = "您的验证码是：%s。请不要把验证码泄露给其他人。" %(params.get("code"))
    ## 请求头
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    ## 构建发送参数
    data = {
        "account": account,
        "password": password,
        "mobile": mobile,
        "content": content,
    }
    ## 发送
    response = requests.post(url, headers=headers, data=data)
    print(response.content.decode())

    return "send code"






from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

import os
from Qshop.settings import BASE_DIR
class MiddleWareTest(MiddlewareMixin):
    def process_request(self,request):
        """
        封杀非法ip
        :param request:  请求对象
        :return:
        """
        # print (request)
        ## REMOTE_ADDR
        # print (request.META["REMOTE_ADDR"])
        req_ip= request.META["REMOTE_ADDR"]
        ## 获取请求的ip  10.10.107.65
        ## 判断ip
        if req_ip == "10.10.107.65":
            return HttpResponse("hello同学，你被禁用了")
        print ("我是 process_request")


        ## request
            ##   对 request携带的参数做预处理
                ## 参数中 是否含有敏感字



        ## 返回响应


    def process_view(self,request, callback, callback_args, callback_kwargs):
        """

        :param request: 请求对象
        :param callback:   对应的视图函数，访问的是那个视图函数，callback就是哪个函数
        :param callback_args:  元祖   视图函数的参数
        :param callback_kwargs:  字典  视图函数的参数
        :return:
        """
        print ("woshi process_view")
        # print(callback)
    # def process_exception(self,request,exception):
    #     """
    #     :param request:
    #     :param exception:
    #     :return:
    #     """
    #     print ("我是 process_exception")
    #     print (exception)
    #     ## 将exception写入文件中   error.log
    #     ##   打开文件
    #     file = os.path.join(BASE_DIR,'error.log')
    #     with open(file,"a") as f:
    #         ## 日志
    #         import time
    #         now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    #         content = "[%s]:%s\n" %(now,str(exception))
    #         ##  写入内容
    #         f.write(content)
    #     ## 写完日志 给boss发送短信/邮件/
    #     ## 发送  异步
    #     # from CeleryTask.tasks import send_email
    #     # params = {
    #     #     "content":"报错了，赶紧解决"
    #     # }
    #     # send_email.delay(params)
    #     return HttpResponse("代码报错了 <br> %s " % exception)
    def process_template_response(self,request,response):
        """

        :param request:
        :param response:
        :return:
        """
        print ("我是 process_temlate_response")
        return response








    def process_response(self,request,response):
        """

        :param request: 请求对象
        :param response:  响应对象
        :return:
        """
        print("我是process_response")
        return response



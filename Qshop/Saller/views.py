from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Saller.models import *
import hashlib
from django.core.paginator import Paginator
# Create your views here.

## 登录装饰器
def LoginVaild(func):
    ## 1. 获取cookie中username和email
    ## 2. 判断username和email
    ## 3. 如果成功  跳转
    ## 4. 如果失败   login.html
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('username')
        ## 获取session
        session_username = request.session.get("username")
        if username and session_username and username == session_username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Saller/login/')
    return inner

## 密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

## 注册
def register(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            ## 判断邮箱是否存在
            loginuser = LoginUser.objects.filter(email=email).first()
            if not loginuser:
                ## 不存在 写库
                user = LoginUser()
                user.email = email
                user.username = email
                user.password = setPassword(password)
                user.save()
            else:
                error_msg = "邮箱已经被注册，请登录"
        else:
            error_msg = "邮箱不可以为空"

    return render(request,"saller/register.html",locals())

## 登录
def login(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                ## 存在
                if user.password == setPassword(password):
                    ## 登录成功
                    ## 跳转页面
                    # error_msg = "登录成功"
                    # return HttpResponseRedirect('/index/')
                    ## 设置cookie
                    response  = HttpResponseRedirect("/Saller/index/")
                    response.set_cookie("username",user.username)
                    response.set_cookie("userid",user.id)
                    request.session['username'] = user.username  ## 设置session
                    return response
                else:
                    error_msg = "密码错误"
            else:
                error_msg = "用户不存在"
        else:
            error_msg = "邮箱不可以为空"
    return render(request,"saller/login.html",locals())

## 首页
@LoginVaild
def index(request):
    return render(request,"saller/index.html")

## 登出
def logout(request):
    # 删除cookie   删除  session
    response = HttpResponseRedirect("/Saller/login/")
    # response.delete_cookie("kename")
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)

    del request.session['username']
    return response
## 商品列表
def goods_list(request,status,page=1):
    """

    :param request:
    :param status: 想要获取的是 在售或者下架的商品   在售传参1   下架是 0
    :param page:   页
    :return:
    """
    page = int(page)
    if status == "0":
        ## 下架商品
        goods_obj = Goods.objects.filter(goods_status = 0).order_by('goods_number')
    else:
        ## 在售商品
        goods_obj = Goods.objects.filter(goods_status = 1).order_by('goods_number')
    goods_all = Paginator(goods_obj,10)
    goods_list = goods_all.page(page)  ##

    return render(request,"saller/goods_list.html",locals())


## 商品状态
def goods_status(request,status,id):
    """
    完成当 下架  修改 status 为 0
    当 上架的   修改status 为 1
    :param request:
    :param status:  操作内容  up 上架    down   下架
     :param id:  商品id
    :return:
    """
    id = int(id)
    goods = Goods.objects.get(id=id)
    if status== "up":
        ###上架
        goods.goods_status = 1
    else:
        ## 下架
        goods.goods_status = 0
    goods.save()
    # return HttpResponseRedirect("/goods_list/1/1/")
    ##  获取请求来源
    url =request.META.get("HTTP_REFERER","/Saller/goods_list/1/1/")
    return HttpResponseRedirect(url)

@LoginVaild
def personal_info(request):
    ##
    user_id = request.COOKIES.get("userid")
    print (user_id)
    user = LoginUser.objects.filter(id = user_id).first()
    if request.method == "POST":
        ## 获取 数据，保存数据
        data = request.POST
        print (data.get("email"))
        user.username = data.get("username")
        user.phone_number = data.get("phone_number")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        user.photo = request.FILES.get("photo")
        user.save()
        print (data)
    return render(request,"saller/personal_info.html",locals())



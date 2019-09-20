from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
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
            return HttpResponseRedirect('/login/')
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

    return render(request,"register.html",locals())

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
                    response  = HttpResponseRedirect("/index/")
                    response.set_cookie("username",user.username)
                    request.session['username'] = user.username  ## 设置session
                    return response
                else:
                    error_msg = "密码错误"
            else:
                error_msg = "用户不存在"
        else:
            error_msg = "邮箱不可以为空"
    return render(request,"login.html",locals())

## 首页
@LoginVaild
def index(request):
    return render(request,"index.html")

## 登出
def logout(request):
    # 删除cookie   删除  session
    response = HttpResponseRedirect("/login/")
    # response.delete_cookie("kename")
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)

    del request.session['username']
    return response

def base(request):
    return render(request,"base.html")
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

    # return render(request,"goods_list.html",locals())
    # return render(request,"vuedemo.html",locals())
    return render(request,"vue_goods_list.html")

## 提供数据的api接口
## 返回的是一个 json对象
def goods_list_api(request,status,page=1):

    page = int(page)
    if status == "0":
        ## 下架商品
        goods_obj = Goods.objects.filter(goods_status = 0).order_by('goods_number')
    else:
        ## 在售商品
        goods_obj = Goods.objects.filter(goods_status = 1).order_by('goods_number')
    goods_all = Paginator(goods_obj,10)
    goods_list = goods_all.page(page)  ##

    res = []
    for one in goods_list:
        res.append({
            "goods_number":one.goods_number,
            "goods_name":one.goods_name,
            "goods_price":one.goods_price,
            "goods_count":one.goods_count,
            "goods_location":one.goods_location,
            "goods_safe_date":one.goods_safe_date,
            "goods_status":one.goods_status,
            "goods_pro_time":one.goods_pro_time,
        })

    result = {
        'data':res,
        "page_range":list(goods_all.page_range),
    }
    return JsonResponse(result)


## 批量生产数据
import random
def add_goods(request):
    goods_name = "菠菜、甜菜、芹菜、胡萝卜、小茴香、芫荽、番茄、茄子、辣椒、黄瓜、西葫芦、南瓜、芜菁、白菜、甘蓝、芥菜 四季豆 豌豆 胡豆 毛豆 土豆 黄豆芽 绿豆芽、豆芽 甘蓝菜 包心菜 大白菜 小白菜 水白菜 西洋菜 通心菜 潺菜 花椰菜 西兰花 空心菜 金针菜 芥菜 芹菜 蒿菜 甜菜 紫菜 生菜 菠菜 韭菜 香菜 发菜 榨菜 雪里红 莴苣 芦笋 竹笋 笋干 韭黄 白萝卜 胡萝卜 荸荠 菜瓜 丝瓜 水瓜 南瓜 苦瓜 黄瓜 青瓜 付子瓜 冬瓜".replace(' ','、')
    goods_name = goods_name.split("、")
    goods_address = "北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省，内蒙古自治区，广西壮族自治区，西藏自治区"
    goods_address = goods_address.split("，")
    ## 添加数据
    for i,j in enumerate(range(100),1):  ## i 是序号 索引
        goods = Goods()
        goods.goods_number = str(i).zfill(5)   ## 返回指定长度的字符串 参数定义了长度
        goods.goods_name = random.choice(goods_address) + random.choice(goods_name)
        goods.goods_price = random.random()*100
        goods.goods_count = random.randint(1,100)
        goods.goods_location = random.choice(goods_address)
        goods.goods_safe_date = random.randint(1,36)
        goods.save()
    return HttpResponse("add goods")

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
    url =request.META.get("HTTP_REFERER","/goods_list/1/1/")
    return HttpResponseRedirect(url)


## 目的 提供页面
def api_goods_list(request):
    return render(request,"api_goods_list.html")

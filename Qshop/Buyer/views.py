from django.shortcuts import render
from Saller.models import *
from Saller.views import setPassword
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect

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
            return HttpResponseRedirect('/Buyer/login/')
    return inner
# Create your views here.
## 首页
def index(request):
    goods_type = GoodsType.objects.all()
    result = []
    for type in goods_type:
        goods = type.goods_set.order_by("-goods_price")
        if len(goods) >= 4:
            goods = goods[:4]
            result.append({"type":type,"goods":goods})
    ## 构建一个返回数据类型   返回满足4条的商品，有4条商品的类型
    return render(request,"buyer/index.html",locals())

def login(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("pwd")
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
                    response  = HttpResponseRedirect("/Buyer/index/")
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

    return render(request,"buyer/login.html")

def register(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        user_name = request.POST.get("user_name")
        if email:
            ## 判断邮箱是否存在
            loginuser = LoginUser.objects.filter(email=email).first()
            if not loginuser:
                ## 不存在 写库
                user = LoginUser()
                user.email = email
                user.username = user_name
                user.password = setPassword(password)
                user.save()
                return HttpResponseRedirect('/Buyer/login/')
            else:
                error_msg = "邮箱已经被注册，请登录"
        else:
            error_msg = "邮箱不可以为空"

    return render(request,"buyer/register.html")
## 登出
def logout(request):
    # 删除cookie   删除  session
    response = HttpResponseRedirect("/Buyer/login/")
    # response.delete_cookie("kename")
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)

    del request.session['username']
    return response

## 商品列表
def goods_list(request):
    """
    根据 keywords传递的类型id，寻找该类型下面的商品
    :param request:
    :return:
    """
    keywords = request.GET.get("keywords")
    print (keywords)
    goods_type = GoodsType.objects.get(id=keywords)
    goods = goods_type.goods_set.all()   ## 反向查询，
    end = len(goods) // 5
    end += 1
    recommend = goods_type.goods_set.order_by("-goods_pro_time")[:end]
    # goods = Goods.objects.all()
    # recommend = Goods.objects.order_by("-goods_pro_time")
    return render(request,"buyer/goods_list.html",locals())



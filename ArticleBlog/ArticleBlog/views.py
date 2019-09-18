from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator


def test(request):
    return HttpResponse("test yemian ")

def about(request):
    return render(request,"about.html")
def index(request):

    ## 获取cookie  获取了用户名
    username = request.COOKIES.get("username")
    print (username)

    """
    查询 6条数据
    查询推荐的7条数据
    查询点击率排行榜的12条数据
    """
    article = Article.objects.order_by("-date")[:6]
    recommend_article = Article.objects.filter(recommend=1).all()[:7]
    click_article = Article.objects.order_by("-click")[:12]

    return render(request,"index.html",locals())
def listpic(request):
    return render(request,"listpic.html")
def newslistpic(request,page=1):
    page = int(page)
    article = Article.objects.order_by("-date")
    paginator = Paginator(article,6)   ##每页显示6条数据
    page_obj = paginator.page(page)
    ## 获取当前页
    current_page = page_obj.number
    start = current_page - 3
    if start < 1:
        start = 0
    end =current_page + 2
    if end > paginator.num_pages:
        end = paginator.num_pages
    if start == 0:
        end = 5
    page_range = paginator.page_range[start:end]
    return render(request,"newslistpic.html",locals())

def base(request):
    return render(request,'base.html')

def articledetails(request,id):
    ## id 为字符串类型
    id = int(id)
    article= Article.objects.get(id=id)
    print (article)
    return render(request,"articledetails.html",locals())


def addarticle(request):

    for x in range(100):
        article = Article()
        article.title = "title_%s" % x
        article.content = "content_%s" % x
        article.description = "description_%s" % x
        article.author = Author.objects.get(id=1)
        article.save()
        article.type.add(Type.objects.get(id=1))
        article.save()
    return HttpResponse("增加数据")

def fytest(request):
    ## 使用django自带分页 Paginator 的时候 原数据要增加排序属性
    article = Article.objects.all().order_by("-date")
    # print(article)
    #  每次显示 5条数据
    paginator = Paginator(article,5)   # 设置每一页显示多少条，返回一个Paginator 对象
    # print (paginator.count)    ##   返回内容总条数
    # print(paginator.page_range)   ## 可迭代的页数
    # print(paginator.num_pages)    ## 最大页数

    page_obj= paginator.page(2)
    print (page_obj)   ##   可以有的页数的数据  表示的当前对象  <Page 20 of 21>
    for one in page_obj:
        print (one.content)

    # print(page_obj.number)   ## 当前页数
    # print(page_obj.has_next())   ## 有没有下一页 返回值  是True 或者 Flase
    # print(page_obj.has_previous())  ## 判断是否有上一页   是True 或者 Flase
    # print(page_obj.has_other_pages())  ## 判断是否有其他页   是True 或者 Flase
    # print(page_obj.next_page_number())  # 返回 下一页的页码   如果没有下一页 抛出异常
    # print(page_obj.previous_page_number())  ## 返回上一页的页码

    return HttpResponse("分页功能测试")



def gender_demo(request):

    author = Author.objects.get(id=1)
    print (author.gender)
    gender = author.get_gender_display()
    print (gender)

    return HttpResponse("性别测试")

def reqtest(request):
    ## 获取get请求传递的参数
    # data = request.GET
    ## 获取post 的请求参数
    data = request.POST
    print (data)
    print (data.get("name"))
    print (type(data.get("name")))
    print (data.get("age"))

    return HttpResponse("姓名：%s年龄%s" %(data.get("name"),data.get("age")))
    # ## request包含请求信息的  请求对象
    # # print (request)
    # print (dir(request))
    # # print (request.COOKIES)
    # # print (request.FILES)
    # print (request.GET)
    # print (request.scheme)
    # print (request.method)
    # print (request.path)
    # print (request.body)
    # # meta = request.META
    # # print (meta)
    # # for key in meta:
    # #     print(key)
    # # print ("_____")
    # # print (request.META.get('OS'))
    # # print (request.META.get('HTTP_USER_AGENT'))
    # # print (request.META.get('HTTP_HOST'))
    # # print (request.META.get('HTTP_REFERER'))
    #
    #
    # return HttpResponse("请求测试")


def formtest(request):
    ## get请求
    # data = request.GET
    # serach = data.get("serach")   ### 文章标题
    # print (serach)
    # ## 通过form提交的数据，判断数据库中是否存在某个文章
    # ## 通过模型进行查询
    # article = Article.objects.filter(title__contains=serach).all()
    # print (article)

    print(request.method)
    data = request.POST
    print (data.get('username'))
    print (data.get("password"))

    return render(request,"formtest.html",locals())
    # return  render_to_response("formtest.html",locals())

import hashlib
def setPassword(password):
    ## 实现一个密码加密
    md5 = hashlib.md5()   ## 创建一个md5 的一个实例对象
    md5.update(password.encode())   ## 进行加密
    result = md5.hexdigest()
    return result

from Article.forms import Register
# def register(request):
#     regiter_form = Register()   ## 创建一个form表单类的实例对象
#     if request.method == "POST":
#         #  获取用户输入的数据
#         # username = request.POST.get("username")
#         username = request.POST.get("name")
#         password= request.POST.get("password")
#         ## 判断是否有数据
#         content = "参数不全"
#         if username and password:
#             user = User()
#             user.name = username
#             ## 加密密码
#             user.password = setPassword(password)
#             user.save()
#             content = "添加成功"
#     return render(request,"register.html",locals())

## 使用form表单进行验证 后端验证
## 验证用户名是否包含 特殊字符  admin
def register(request):
    regiter_form = Register()   ## 创建一个form表单类的实例对象
    error = ""
    if request.method == "POST":
        data = Register(request.POST)  ## 将post请求传递过来的数据，交给 form表单类进行校验
        if data.is_valid():   ## 判断校验是否通过，  如果通过 返回一个True 否则 是Flase
            clean_data = data.cleaned_data   ### 返回一个字典类型，数据通过校验的数据
            ## 获取到数据，写库
            username = clean_data.get("name")
            password = clean_data.get("password")
            user = User()
            user.name = username
            ## 加密密码
            user.password = setPassword(password)
            user.save()
            error = "添加数据成功"
        else:
            error = data.errors
            print (error)
    return render(request,"register.html",locals())

from Article.forms import *
def cspost(request):
    form_cspost = csforms()  ## 创建一个实例对象
    if request.method =="POST":
        clean_data = csforms(request.POST)
        if clean_data.is_valid():   ### 校验成功   返回  True
            data = clean_data.cleaned_data   ##
            # username = request.POST.get("username")
            username = data.get("username")
            # print (username)
            ## 校验用户   添加用户  等等
            ## 操作数据库
            content = "成功"
        else:
            content = clean_data.errors
    return render(request,"cspost.html",locals())


def ajax_get(request):
    return render(request,"ajax_get.html")
## ajax 完成一个 校验用户名  密码的案例
def ajax_get_data(request):
    result = {"code":10000,"content":""}
    data = request.GET
    username = data.get("username")
    password = data.get("password")
    if username is None or password is None:
        result['code'] = 10001
        result['content'] = "请求参数为空"
    else:
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            result['code'] = 10000
            result['content'] = "用户可登陆"
        else:
            result['code'] = 10002
            result['content'] = "用户不存在或者密码不正确"
    ##  返回一个json对象
    return JsonResponse(result)
    # return HttpResponse("这个是ajax提交数据")

def ajax_post(request):
    ## 调用页面
    return render(request,"ajax_post.html")
def ajax_post_data(request):
    ## 注册
    result = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    if len(username) == 0 or len(password) == 0:
        result["code"] = 10001
        result["content"] = '请求参数为空'
    else:
        ## 添加用户
        user= User()
        user.name = username
        user.password= setPassword(password)
        try:
            user.save()
            result["code"] = 10000
            result["content"] = '添加数据成功'
        except:
            result["code"] = 10002
            result["content"] = '添加数据错误'
    ## 注册
    return JsonResponse(result)


def checkusername(request):
    result = {'code':10001,"content":""}
    #get 请求
    username= request.GET.get("name")
    print (username)
    # 判断用户是否存在
    user = User.objects.filter(name=username).first()
    if user:
        ## 存在
        result = {'code': 10001, "content": "用户名已存在"}
    else:
        result = {'code': 10000, "content": "用户名不存在"}


    return JsonResponse(result)


## 重定向   300问题
from django.http import HttpResponseRedirect
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ##校验
        user = User.objects.filter(name=username).first()
        if user:
            ### 用户存在
            if user.password == setPassword(password):
                ## 密码正确
                ## 跳转首页   状态码   300 重定向
                # return HttpResponse("登录成功")
                # return HttpResponseRedirect("/index/")
                response = HttpResponseRedirect('/index/')
                ## 下发cookie  设置cookie
                response.set_cookie("username",username)

                return response

    return render(request,"login.html")




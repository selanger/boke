from django.http import HttpResponse
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator


def test(request):
    return HttpResponse("test yemian ")

def about(request):
    return render(request,"about.html")
def index(request):
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
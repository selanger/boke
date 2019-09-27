from django.shortcuts import render
from Saller.models import *
from Saller.views import setPassword
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from Buyer.models import *
from alipay import AliPay
from Qshop.settings import alipay_private_key_string,alipay_public_key_string


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
            user = LoginUser.objects.filter(email=email,user_type=1).first()
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

    return render(request,"buyer/login.html",locals())

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
    req_type    完成判断请求
        当 req_type = search
            keywords 商品的名字
        当 req_type = findall
            keywords传递的类型id，寻找该类型下面的商品
    :param request:
    :return:
    """
    keywords = request.GET.get("keywords")
    req_type = request.GET.get("req_type")
    if req_type == "findall":
        ##   查看更多
        goods_type = GoodsType.objects.get(id=keywords)
        goods = goods_type.goods_set.all()   ## 反向查询，
    elif req_type == "search":
        ### 搜索功能
        goods = Goods.objects.filter(goods_name__contains=keywords).all()
    ## 从 商品集中切片
    end = len(goods) // 5
    end += 1
    recommend = goods.order_by("-goods_pro_time")[:end]
    return render(request,"buyer/goods_list.html",locals())

def detail(request,id):
    goods = Goods.objects.get(id=int(id))
    return render(request,"buyer/detail.html",locals())

##个人中心
@LoginVaild
def user_center_info(request):
    return render(request,"buyer/user_center_info.html",locals())


import time
## 订单页面
@LoginVaild
def place_order(request):
    ## 保存订单
    goods_id = request.GET.get("goods_id")      # 商品id
    goods_count = request.GET.get("goods_count")   ## 订单数量
    user_id = request.COOKIES.get("userid")
    if goods_id and goods_count:
        goods_id = int(goods_id)
        goods_count = int(goods_count)
        goods = Goods.objects.get(id=goods_id)
        ## 保存订单表
        payorder = PayOrder()
        order_number = str(time.time()).replace('.','')     ## 生产订单编号
        payorder.order_number = order_number   ## 订单编号
        payorder.order_status = 0
        payorder.order_total = goods.goods_price * goods_count
        payorder.order_user = LoginUser.objects.get(id = user_id)
        payorder.save()
        ## 保存订单详情表
        orderinfo = OrderInfo()
        orderinfo.order_id = payorder
        orderinfo.goods = goods
        orderinfo.goods_count = goods_count
        orderinfo.goods_price = goods.goods_price
        orderinfo.goods_total_price = goods.goods_price * goods_count
        orderinfo.store_id = goods.goods_store
        orderinfo.save()


        total_count = 0
        all_goods_info = payorder.orderinfo_set.all()
        for one in all_goods_info:
            total_count += one.goods_count

    return render(request,"buyer/place_order.html",locals())



@LoginVaild
def place_order_more(request):
    data = request.GET
    userid = request.COOKIES.get("userid")
    #   {'count_11': ['1'], 'goods_13': ['on'], 'count_17': ['1'], 'goods_17': ['on'], 'count_13': ['1']}
    print (data)
    ## 区分   通过获取前端get请求的参数，找到goods_id 和对应的数量
    ## startwith  以goods开始的key
    data_item = data.items()
    request_data = []  ##   [(),(),()]
    for key,value in data_item:
        # print ("%s-------%s"%(key,value))     key : goods_商品id_购物车id
        if key.startswith("goods"):
            goods_id = key.split("_")[1]
            count = request.GET.get("count_"+goods_id)
            cart_id = key.split("_")[2]
            # print("%s ++++++++  %s" %(goods_id,count))
            request_data.append((int(goods_id),int(count),int(cart_id)))
    print (request_data)
    if request_data:
        ## 保存数据
        ##   保存订单表   订单详情表
        ## 订单  保存一笔订单
        payorder = PayOrder()
        order_number = str(time.time()).replace('.','')     ## 生产订单编号
        payorder.order_number = order_number   ## 订单编号
        payorder.order_status = 0
        # payorder.order_total = 所有商品的小计之和
        payorder.order_total = 0
        payorder.order_user = LoginUser.objects.get(id = userid)
        payorder.save()
        order_total = 0
        total_count = 0  ## 商品总数量
        ## 订单详情   保存多条，一种商品一条数据
        for goods_id_one,count_one,cart_id in request_data:
            ## 遍历到一条订单中的多条商品的id 和对应的数量
            goods = Goods.objects.get(id =goods_id_one)
            orderinfo = OrderInfo()
            orderinfo.order_id = payorder
            orderinfo.goods = goods
            orderinfo.goods_count = count_one
            orderinfo.goods_price = goods.goods_price
            orderinfo.goods_total_price = goods.goods_price * count_one
            orderinfo.store_id = goods.goods_store
            orderinfo.save()
            order_total += goods.goods_price * count_one
            total_count += count_one

            cart = Cart.objects.get(id = cart_id)
            cart.order_number = order_number
            cart.save()


        payorder.order_total = order_total
        payorder.save()

    return render(request,"buyer/place_order.html",locals())








def AlipayViews(request):
    order_id = request.GET.get("order_id")    ## 订单id
    payorder = PayOrder.objects.get(id=order_id)
    ## 实例化支付对象
    alipay = AliPay(
        appid='2016101300673550',
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
    )
    ## 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        subject='天天生鲜',  ## 交易主题
        out_trade_no=payorder.order_number,  ## 订单号
        total_amount=str(payorder.order_total),  ## 交易总金额
        return_url="http://127.0.0.1:8000/Buyer/payresult/",  ##  请求支付，之后及时回调的一个接口
        notify_url="http://127.0.0.1:8000/Buyer/payresult/"  ##  通知地址，
    )
    ##   发送支付请求
    ## 请求地址  支付网关 + 实例化订单
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    print(result)

    return HttpResponseRedirect(result)

def payresult(request):

    ## 通过get获取支付宝传递参数，获取其中的订单号，修改订单的状态
    order_number = request.GET.get("out_trade_no")
    paryorder = PayOrder.objects.get(order_number=order_number)
    paryorder.order_status = 1
    paryorder.save()
    return render(request,"buyer/payresult.html",locals())

## 添加购物车
@LoginVaild
def add_cart(request):
    """
    使用post请求，完成添加购物车功能
    :param request:  goods_id(商品id)    count(数量）
    :return:  json  code   msg
    """
    result = {"code":10001,"msg":""}
    if request.method == "POST":
        goods_id = request.POST.get("goods_id")
        count = float(request.POST.get("count",1))   ##  1 为默认值
        user_id = request.COOKIES.get("userid")
        goods = Goods.objects.get(id=goods_id)
        cart = Cart()
        cart.goods_number = count
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price * count
        cart.goods= goods
        cart.cart_user = LoginUser.objects.get(id=user_id)
        cart.save()
        result["code"] = 10000
        result["msg"] = "添加购物车成功"
    else:
        result["code"] = 10001
        result["msg"] = "请求方式不正确"
    return JsonResponse(result)
@LoginVaild
def cart(request):
    user_id = request.COOKIES.get("userid")
    ## 查询购物车中商品
    cart_list = []
    cart = Cart.objects.filter(cart_user_id=user_id,).order_by("-id")   ## 倒序
    count = cart.count()  ## 获取条数   10
    for one in cart:
        if one.order_number != '0':
            ## 说明有订单号  订单状态不为 已支付
            payorder = PayOrder.objects.get(order_number=one.order_number)
            if payorder.order_status != 1:
                ###  已支付的订单
                cart_list.append(one)
            else:
                count -=1    ##  10 -1

        else:
            cart_list.append(one)

    return render(request,"buyer/cart.html",locals())

@LoginVaild
def user_center_order(request):
    user_id = request.COOKIES.get("userid")
    ## 通过用户  获取该用户所有订单
    user = LoginUser.objects.get(id=user_id)
    paryorder = user.payorder_set.order_by("-order_date",'order_status')
    return render(request,"buyer/user_center_order.html",locals())







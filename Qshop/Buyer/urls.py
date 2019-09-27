from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path("login/",login),
    path("index/",index),
    path("register/",register),
    path("logout/",logout),
    path("goods_list/",goods_list),
    path("user_center_info/",user_center_info),
    path("place_order/",place_order),
    path("alipayviews/",AlipayViews),
    path("payresult/",payresult),
    path("add_cart/",add_cart),
    path("cart/",cart),
    path("place_order_more/",place_order_more),
    path("user_center_order/",user_center_order),
    re_path("detail/(?P<id>\d+)",detail),

    ###  path("Saller/",include("Saller.urls")),
]

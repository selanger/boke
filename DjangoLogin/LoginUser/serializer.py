from rest_framework import serializers
from LoginUser.models import *

class GoodsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:   ## 元类
        model = Goods   ### 遍历的对象
        fields = [
            "id",
            "goods_number",
            "goods_name",
            "goods_price",
            "goods_count",
            "goods_location",
            "goods_safe_date",
            "goods_status",
            "goods_pro_time"
        ]   ## 返回的字段


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:   ## 元类
        model = LoginUser   ### 遍历的对象
        fields = [
            "id",
            "email",
            "password",
            "username",
            "phone_number",
            "photo",
            "age",
            "gender",
            "address"
        ]   ## 返回的字段


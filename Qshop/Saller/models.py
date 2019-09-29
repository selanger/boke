from django.db import models

# Create your models here.
class LoginUser(models.Model):
    ## id 不需要写
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32,null=True,blank=True)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    photo = models.ImageField(upload_to="images",null=True,blank=True)   ## /static/images
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(null=True,blank=True,max_length=4)
    address = models.TextField(null=True,blank=True)
    ### 0 代表的卖家 1 代表买家 2 管理员
    user_type = models.IntegerField(default=1)

    ###  null 针对数据库，表示可以为空，即在数据库的存储中可以为空
    ### blank 针对表单，表示在表单中该字段可以不填，但是对数据库没有影响

### 类型模型
class GoodsType(models.Model):
    type_label = models.CharField(max_length=32)
    type_description = models.TextField()
    type_picture = models.ImageField(upload_to="images")

class Goods(models.Model):
    goods_number = models.CharField(max_length=11,verbose_name="商品编号")
    goods_name = models.CharField(max_length=32,verbose_name="商品的名字")
    goods_price = models.FloatField(verbose_name="价格")
    goods_count = models.IntegerField(verbose_name="数量")
    goods_location = models.CharField(max_length=254,verbose_name="产地")
    goods_safe_date = models.IntegerField(verbose_name="保质期")
    goods_status = models.IntegerField(verbose_name="状态")  ## 0 代表下架  1 代表在售
    goods_pro_time = models.DateField(auto_now=True,verbose_name="生产日期")
    picture = models.ImageField(upload_to="images")   ## 商品图片
    goods_description = models.TextField(default="好好。。。。。")
    ## 类型  一对多
    goods_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,default=1)
    ## 店铺 一对多
    goods_store = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,default=1)


class Vaild_Code(models.Model):
    code_content = models.CharField(max_length=8,verbose_name="验证码")
    code_time = models.CharField(max_length=32,verbose_name="创建时间")
    code_status = models.IntegerField(verbose_name="状态")    ##1 使用  0 未使用
    code_user = models.EmailField(verbose_name="邮箱")







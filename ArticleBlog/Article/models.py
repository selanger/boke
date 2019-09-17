from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

GENDER_LIST = (
    (1,'男'),
    (2,"女"),
)
class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name="作者名字")
    age = models.IntegerField(verbose_name="年龄")
    # gender = models.CharField(max_length=8,verbose_name="性别")    ## 男  女
    gender = models.IntegerField(choices=GENDER_LIST, verbose_name="性别",default=1)    ## 1 男  2 女
    email = models.CharField(max_length=32,verbose_name="邮箱")

    def __str__(self):
        return self.name

    class Meta:
        db_table='author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name


class Type(models.Model):
    name = models.CharField(max_length=32,verbose_name="类型名字")
    description = models.TextField(verbose_name="类型描述")
    def __str__(self):
        return self.name

    class Meta:
        db_table='type'
        verbose_name = '类型'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='文章标题')
    date = models.DateField(auto_now=True,verbose_name='日期')
    # content = models.TextField(verbose_name='文章内容')
    content = RichTextField()
    # description = models.TextField(verbose_name='文章描述')
    description = RichTextField()
    ## 图片类型
    ## upload_to 指定文件上传位置    static目录下的  images 目录中
    picture = models.ImageField(upload_to='images')
    # 推荐
    recommend = models.IntegerField(verbose_name="推荐",default=0)   ## 0 代表不推荐  1代表推荐
    # 点击率
    click = models.IntegerField(verbose_name="点击率",default=0)
    author = models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1)
    type = models.ManyToManyField(to=Type)

    def __str__(self):
        return self.title
    class Meta:
        db_table='article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


    class Meta:
        db_table = 'user'







from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    gender = models.CharField(max_length=8)
    email = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table='author'


class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    def __str__(self):
        return self.name

    class Meta:
        db_table='type'


class Article(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)
    content = models.TextField()
    description = models.TextField()
    author = models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1)
    type = models.ManyToManyField(to=Type)

    def __str__(self):
        return self.title
    class Meta:
        db_table='article'



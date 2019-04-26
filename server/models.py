from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 10, null = False)
    password = models.CharField(max_length = 20, null = False)
    total = models.IntegerField(default = 0)
    like = models.IntegerField(default = 0)
    imgUrl = models.URLField(default='https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2905424204,1949750727&fm=26&gp=0.jpg')
    name = models.CharField(max_length = 20)
class Passage(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 2000)
    pic = models.URLField()
class Search(models.Model):
    id = models.AutoField(primary_key = True)
    search = models.CharField(max_length = 20)
    times = models.IntegerField(default = 0)
class Home(models.Model):
    id = models.AutoField(primary_key = True)
    pic = models.URLField()
    types = models.CharField(max_length = 20)
class Topic(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20)
    img = models.URLField()

from django.db import models
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.fields import ThumbnailerImageField


# 继承AbstractUser,可以扩展字段还可以使用
class User(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name='手机号')
    realname = models.CharField(max_length=8, verbose_name="真实姓名",null=True,blank=True)
    qq = models.CharField(max_length=11, verbose_name="QQ号",null=True,blank=True)
    avator_sor = models.ImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")
    avator = ThumbnailerImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")

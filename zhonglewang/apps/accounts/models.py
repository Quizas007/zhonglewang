from django.db import models
from django.contrib.auth.models import AbstractUser


# 继承AbstractUser,可以扩展字段还可以使用
class User(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name='手机号')
    avator_sor = models .ImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")


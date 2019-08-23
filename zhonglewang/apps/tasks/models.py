from django.db import models
from django.contrib.auth.models import User
from zhonglewang.settings import AUTH_USER_MODEL
from django.utils import timezone
# 含文件上传(富文本编辑器)
from ckeditor_uploader.fields import RichTextUploadingField
from .validator import valid_mode
# django-taggit
from taggit.managers import TaggableManager
from PIL import Image


# 类别
class Category(models.Model):
    # 分类名
    name = models.CharField(verbose_name="分类名",max_length=128)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# 任务模型
class Tasks(models.Model):
    MODE_CHOICES = (
        (1, "自由模式"),
        (2, "担保模式"),
    )
    # 任务发布者
    publisher = models.ForeignKey(AUTH_USER_MODEL,verbose_name="发布者")
    # 任务标题
    title = models.CharField(verbose_name="任务标题",max_length=128)
    # 任务标题图
    avatar = models.ImageField(upload_to='tasks/%Y%m%d/',blank=True)
    # 任务内容(使用富文本编辑器)
    content = RichTextUploadingField(verbose_name="任务内容")
    # 任务模式
    mode = models.IntegerField(verbose_name="模式",choices=MODE_CHOICES,validators=[valid_mode])
    # 酬劳
    reward = models.PositiveIntegerField(verbose_name="酬劳",default=0)
    # 发布时间
    created = models.DateTimeField(verbose_name="发布时间",default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(verbose_name="更新时间",auto_now=True)
    # 浏览量
    total_views = models.PositiveIntegerField(verbose_name="浏览量",default=0)
    # 添加类别
    category = models.ForeignKey(Category,verbose_name="类别",on_delete=models.CASCADE,null=True)
    # 添加标签
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name
        permissions = (
                          ('can_change_task', "可以修改任务信息"),
                          ('can_add_task', "可以添加任务信息"),
                      )

    # 保存时处理图片
    def save(self,*args,**kwargs):
        # 调用原有的save()
        task = super(Tasks,self).save(*args,**kwargs)
        # 固定宽度缩放图片
        if self.avatar and not kwargs.get('update_filed'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 160
            new_y = int(new_x * (y/x))
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return task


    def __str__(self):
        return self.title


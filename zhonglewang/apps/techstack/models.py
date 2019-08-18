from django.db import models
from apps.accounts.models import User
# timezone用于处理时间相关事务
from django.utils import timezone
from ckeditor.fields import RichTextField
# 含文件上传
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    """分类"""
    name = models.CharField("分类名称", max_length=64)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    """标签"""
    name = models.CharField("标签名", max_length=64)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Articles(models.Model):
    """文章表"""
    title = models.CharField(verbose_name="文章标题", unique=True, max_length=256)
    author = models.ForeignKey(User,verbose_name="文章作者",on_delete=models.CASCADE)
    # body = models.TextField(verbose_name="文章正文")
    body = RichTextUploadingField(verbose_name="文章正文",null=True)
    status = models.BooleanField(verbose_name="审核状态", default=False)
    created = models.DateTimeField(verbose_name="创建时间",default=timezone.now)
    # 参数auto_now=True指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(verbose_name="更新时间",auto_now=True)
    category = models.ForeignKey(Category, verbose_name="所属分类", null=True,on_delete=models.CASCADE)
    # 数组....(会产生一个中间表)
    tag = models.ManyToManyField(Tag, verbose_name="文章标签")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        permissions = (
                          ('can_change_article', "可以修改文章信息"),
                          ('can_add_article', "可以添加文章信息"),
                      )

    def __str__(self):
        return self.title

class ArticlesCollection(models.Model):
    """收藏文章"""
    article = models.ForeignKey(Articles, verbose_name="文章", related_name='articles_collection_set')
    user = models.ForeignKey(User, verbose_name="收藏者", related_name='articles_collection_set')
    create_time = models.DateTimeField("收藏/取消时间", auto_now=True)
    # True表示收藏 ,False表示未收藏
    status = models.BooleanField("收藏状态", default=True)

    class Meta:
        verbose_name = "收藏记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.status: ret="收藏"
        else:
            ret="取消收藏"
        return f"{self.user}:{ret}:{self.article.title}"




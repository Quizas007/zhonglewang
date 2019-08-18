from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.techstack.models import Articles,ArticlesCollection
from libs import sms
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import logging
logger = logging.getLogger("apis")

# 生成短信验证码，并写入cache
def mobile_captcha(request):
    ret = {"code": 200, "msg": "验证码发送成功！"}
    try:
        mobile = request.GET.get("mobile")
        if mobile is None: raise ValueError("手机号不能为空！")
        mobile_captcha = "".join(random.choices('0123456789', k=6))
        from django.core.cache import cache
        # 将短信验证码写入redis, 300s 过期
        cache.set(mobile, mobile_captcha, 300)
        if not sms.send_sms(mobile, mobile_captcha):
            raise ValueError('发送短信失败')
    except Exception as ex:
        ret = {"code": 400, "msg": "验证码发送失败！"}
    return JsonResponse(ret)

# 获取文章
class ArticlesView(View):
    def get(self, request):
        """
        :param request:
        :return:
        # /apis/articles/?order=asc&offset=0&limit=25
        # /apis/articles/?pagesize=25&offset=0&page=1&grade=4&category=1&status=1
        """
        # 获取参数
        page = int(request.GET.get("page", 1))
        pagesize = int(request.GET.get("pagesize", 25))
        offset = int(request.GET.get("offset", 0))
        category = int(request.GET.get("category",0))
        search = request.GET.get("search")

        # 取出所有数据，筛选指定等级和分类
        articles_list = Articles.objects.all()
        if search:
            articles_list = articles_list.filter(title__icontains=search)
        if search:
            if search.isdigit():
                articles_list = articles_list.filter(
                    Q(id=search) | Q(body__icontains=search) | Q(title__icontains=search))
            else:
                articles_list = articles_list.filter(Q(body__icontains=search) | Q(title__icontains=search))


        if category: 
            articles_list = articles_list.filter(category__id=category)
        logger.info(articles_list)
        # 筛选状态 => 我的答题表
        articles_list = articles_list.values('id', 'title', 'author__username')


        total = len(articles_list)

        # 计算当前页面的数据
        articles_list = articles_list[offset:offset + pagesize]

        # 用于计算当前登录的用户是否收藏对应的题目，如果收藏实心True，没有收藏空心False
        for item in articles_list:
            item["collection"] = True if ArticlesCollection.objects.filter(
                user=request.user, status=True, article_id=item["id"]) else False

        # 格式是bootstrap-table要求的格式
        articles_dict = {'total': total, 'rows': list(articles_list)}
        return JsonResponse(articles_dict)

# 收藏文章
class ArticleCollectionView(LoginRequiredMixin, View):
    def get(self, request, id):
        """
        当用户点击该文章时，首先获取该题文章，并检查该文章是否已被操作过
        修改当前文章的收藏状态
        返回json数据
        id => 题目的ID
        """
        article = Articles.objects.get(id=id)
        result = ArticlesCollection.objects.get_or_create(user=request.user, article=article)
        # result是一个元组，第一参数是instance, 第二个参数是true和false
        # True表示新创建,False表示老数据
        article_collection = result[0]
        if not result[1]:
            # print('x',answer_collection.status)
            if article_collection.status:
                article_collection.status=False
            else:
                article_collection.status=True
            article_collection.save()
        msg = model_to_dict(article_collection)
        ret_info = {"code":200, "msg":msg}
        return JsonResponse(ret_info)
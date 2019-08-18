from django.shortcuts import render
from django.views.generic import View,DetailView
from .models import Category,Articles
from django.contrib.auth.mixins import LoginRequiredMixin

class ArticlesList(LoginRequiredMixin,View):
    def get(self, request):
        category = Category.objects.all().values("id", "name")
        search = request.GET.get("search","")
        kwgs = {
            "category": category,
            "search": search,
        }
        return render(request, 'articles.html', kwgs)

def test(request):
    pass

class ArticleDetail(DetailView):
    model = Articles
    pk_url_kwarg = 'id'
    template_name = "article_detail.html"
    # 默认名：object
    context_object_name = "object"

    # 额外传递my_answer
    def get_context_data(self, **kwargs):
        # kwargs：字典、字典中的数据返回给html页面
        # self.get_object() => 获取当前id的数据（问题）
        question = self.get_object()  # 当前这道题目
        return super().get_context_data(**kwargs)

    def post(self, request, id):
        from django.db import transaction
        try:
            with transaction.atomic():
                # 没有回答过。create
                # 更新回答。get->update
                # 获取对象，没有获取到直接创建对象
                new_answer = Answers.objects.get_or_create(question=self.get_object(), user=self.request.user)
                # 元组：第一个元素获取/创建的对象， True（新创建）/False（老数据）
                new_answer[0].answer = request.POST.get("answer", "没有提交答案信息")
                new_answer[0].save()
                # OPERATE = ((1, "收藏"), (2, "取消收藏"), (3, "回答"))
                UserLog.objects.create(user=request.user, operate=3, question=self.get_object())
                my_answer = json.loads(serializers.serialize("json", [new_answer[0]]))[0]["fields"]
            msg = "提交成功"
            code = 200
        except Exception as ex:
            logger.error(ex)
            my_answer = {}
            msg = "提交失败"
            code = 500

        result = {"status": code, "msg": msg, "my_answer": my_answer}
        return JsonResponse(result)
from django.shortcuts import render,redirect,reverse
from django.views.generic import View,DetailView
from .models import Category,Articles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ArticleCreateForm

# 展示所有文章
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

# 展示文章详情
def article_detail(request,id):
    # 取出对应的文章
    article = Articles.objects.get(id=id)
    # 浏览量+1
    article.total_views+=1
    article.save(update_fields=['total_views'])
    # 参数
    kwgs = {
        'article':article
    }
    return render(request,'article_detail.html',kwgs)

# 发表文章
class ArticleCreate(View):
    def get(self,request):
        article_create_form = ArticleCreateForm()
        context = {'article_create_form':article_create_form}
        return render(request,'article_create.html',context)
    def post(self,request):
        article_create_form = ArticleCreateForm(data=request.POST)
        if article_create_form.is_valid():
            new_article = article_create_form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return redirect(reverse("techstack:articles"))
        else:
            return HttpResponse("表单内容有误，请重新填写。")

# 删除文章
@login_required
def article_delete(request,id):
    article = Articles.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，您无权删除此文章")
    article.delete()
    return redirect(reverse("techstack:articles"))

# 修改文章
class ArticleUpdate(LoginRequiredMixin,View):
    def get(self,request,id):
        article = Articles.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章")
        article_post_form = ArticleCreateForm()
        context = {'article':article,'article_post_form':article_post_form}
        return render(request,'article_update.html',context)

    def post(self,request,id):
        article = Articles.objects.get(id=id)
        article_post_form = ArticleCreateForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect(reverse("article:article_detail"),id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")




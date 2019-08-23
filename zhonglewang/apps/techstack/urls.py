from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # 展示所有文章
    url(r'^articles/$',views.ArticlesList.as_view(),name="articles"),
    # 测试
    url(r'article/$', views.test, name="article"),
    # 展示文章详情
    url(r'^article/(?P<id>\d+)/$', views.article_detail,name="article_detail"),
    # 发表文章
    url(r'^article_create/$',views.ArticleCreate.as_view(),name="article_create"),
    # 删除文章
    url(r'^article_delete/(?P<id>\d+)$',views.article_delete,name="article_delete"),
    # 修改文章
    url(r'^article_update/(?P<id>\d+)',views.ArticleUpdate.as_view(),name="article_update")

]
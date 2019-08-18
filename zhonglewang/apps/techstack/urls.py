from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^articles/$',views.ArticlesList.as_view(),name="articles"),
    url(r'article/$', views.test, name="article"),
    url(r'^article/(?P<id>\d+)/$', views.ArticleDetail.as_view(),name="article_detail"),
]
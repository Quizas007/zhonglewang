from django.conf.urls import url
from . import views


urlpatterns = [
    # 获取手机验证码
    url(r'^mobile_captcha/$',views.mobile_captcha,name="mobile_captcha"),
    # 获取文章
    url(r'^articles/$', views.ArticlesView.as_view(), name="articles"),
    # 收藏文章
    url(r'^article/collection/(?P<id>\d+)/$', views.ArticleCollectionView.as_view(), name='question_collection'),


]
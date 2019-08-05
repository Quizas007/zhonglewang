from django.conf.urls import url
from . import views


urlpatterns = [
    # 获取手机验证码
    url(r'^mobile_captcha/$',views.mobile_captcha,name="mobile_captcha"),

]
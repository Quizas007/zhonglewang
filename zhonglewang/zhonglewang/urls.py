"""zhonglewang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^accounts/',include('apps.accounts.urls',namespace="accounts")),
    url(r'^apis/',include('apps.apis.urls',namespace="apis")),
    url(r'^techstack/',include('apps.techstack.urls',namespace="techstack")),
    url(r'^tasks/',include('apps.tasks.urls',namespace="tasks")),
    url(r'^usercenter/',include('apps.usercenter.urls',namespace="usercenter")),
    # meida 处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # ckeditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # chat
    url(r'^chat/',include("apps.chat.urls",namespace="chat")),
]

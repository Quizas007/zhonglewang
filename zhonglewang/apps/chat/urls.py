from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.chat_index, name='chat_index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
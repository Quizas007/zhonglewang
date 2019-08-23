from django.conf.urls import url
from django.views import View
from . import views

urlpatterns = [
    url(r'^freelist/$',views.freelist,name="freelist"),
    url(r'^securitylist/$',views.securitylist,name="securitylist"),
    url(r'^create/$',views.TaskCreate.as_view(),name="create"),
    url(r'^free_detail/(?P<id>\d+)/$',views.free_detail,name="free_detail"),
    url(r'^security_detail/(?P<id>\d+)/$',views.security_detail,name="security_detail"),
]
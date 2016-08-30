

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^qiniu/$', views.QiniuAPIView.as_view()),
]

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.videochat),
    url(r'register/$',views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'chat/$', views.chat, name='chat'),
]


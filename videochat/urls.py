from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'register/$',views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'profile/$', views.user_profile, name='profile'),
    url(r'logout/$', views.user_logout, name='logout'),
    #url(r'chat/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.chat, name='chat'),
    url(r'chat/([0-9]{5})',views.chat, name='chat'),
    url(r'update_status/$', views.update_status, name='update_status'),
    url(r'edit_contact/([^@]+@[^@]+\.[^@]+)', views.edit_contact, name='edit_contact'),
    url(r'add_contact/$', views.add_contact, name='add_contact'),
]


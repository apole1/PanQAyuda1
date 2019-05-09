from django.conf.urls import url
from django.urls import path
from core import views

app_name = 'core'

urlpatterns=[
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]
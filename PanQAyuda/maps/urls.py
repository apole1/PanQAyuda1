from django.conf.urls import url
from maps import views


app_name = 'maps'

urlpatterns = [
    url(r'', views.default_map, name="default"),
]
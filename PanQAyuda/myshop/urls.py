from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name= 'logout'),
    url('social-auth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

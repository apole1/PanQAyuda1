from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('account/', include('django.contrib.auth.urls')),
    
    #SOCIAL LOGIN
    path("login/", views.social_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("social/", views.home, name="home"),
    path('maps/', include('maps.urls', namespace="maps")),

    #USER LOGIN
    url(r'^signin/',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^core/',include('core.urls')),
    url(r'^user_logout/$', views.user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

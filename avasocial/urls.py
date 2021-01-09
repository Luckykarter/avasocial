"""avasocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from avasocial.views import swagger
from socialnetwork import views
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView


schema_view = get_schema_view(
   openapi.Info(
      title="AVA Social Network",
      default_version='v1',
      description="Egor Wexler\'s home assignment",
      contact=openapi.Contact(email="egor.wexler@icloud.com"),
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', views.profile_view, name='user_profile'),

    path("", include("socialnetwork.urls")),
    path("", views.index),
    path("accounts/login/", views.login_view),
    path("accounts/logout/", views.logout_view),
    path("accounts/signup/", views.signup_view),


    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]




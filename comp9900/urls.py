"""comp9900 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterguesns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from airbnb import views
from django.conf.urls import url

urlpatterns = [
    url(r'userRegister/', views.userRegister, name="userRegister"),
    url(r'userLogin/', views.userLogin, name="userLogin"),
    url(r'index/', views.index, name="index"),
    url(r'logout/', views.logout, name='logout'),
    url(r'updateUserInfo', views.updateUserInfo, name="updateUserInfo"),
    url(r'portraitUpload', views.portraitUpload, name="portraitUpload")
]

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
from django.urls import path

urlpatterns = [
    path('userRegister/', views.userRegister, name="userRegister"),
    path('userLogin/', views.userLogin, name="userLogin"),
    path('index/', views.index, name="index"),
    path('', views.index, name="index"),
    path('logout/', views.logout, name='logout'),
    path('updateUserInfo/', views.updateUserInfo, name="updateUserInfo"),
    path('portraitUpload/', views.portraitUpload, name="portraitUpload"),
    path('listingAdd/listingStart', views.listingStart, name='listingStart'),
    path('listingAdd/amenities', views.amenities, name='amenities'),
    path('listingAdd/scene', views.scene, name='scene'),
    path('listingAdd/description', views.description, name='description'),
    path('listingManage/', views.listingManage, name='listingManage'),
    path('listingAdd/location', views.location, name='location'),
    path('calendar', views.calendar, name='calendar'),
]

from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^get_valid_img/', views.get_valid_img),
    url(r'^index/', views.index),
    url(r'^register/', views.register),
]
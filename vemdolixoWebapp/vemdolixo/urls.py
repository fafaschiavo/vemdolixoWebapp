from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generic-register/', views.generic_register_create, name='generic_register_create'),
]
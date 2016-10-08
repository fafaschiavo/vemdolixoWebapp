from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^generic-register/', views.generic_register_create, name='generic_register_create'),
    url(r'^simple-register/', views.simple_register_create, name='simple_register_create'),
    url(r'^new-search/', views.new_search, name='new_search'),
    url(r'^footer-form/', views.footer_form, name='footer_form'),
    url(r'^about/', views.about, name='about'),
    url(r'^great-amounts/', views.great_amounts, name='great_amounts'),
    url(r'^great-amounts-send-email/', views.great_amounts_send_email, name='great_amounts_send_email'),
]
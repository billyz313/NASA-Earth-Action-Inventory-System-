from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.inventory, name='inventory'),
    path('asset/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('privacy', views.index, name='privacy'),

    path('terms', views.index, name='terms'),
    path('contact', views.index, name='contact'),

    path('about', views.index, name='about'),

]

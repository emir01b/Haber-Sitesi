from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('weather/', views.weather, name='weather'),
]

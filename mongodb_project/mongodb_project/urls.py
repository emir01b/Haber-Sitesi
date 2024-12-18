# mongodb_app/urls.py

from django.contrib import admin
from django.urls import path
from mongodb_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Ana sayfa
    path('dunya/', views.dunya, name='dunya'),  # Dünya haberleri
    path('ekonomi/', views.ekonomi, name='ekonomi'),  # Ekonomi haberleri
    path('havadurumu/', views.havadurumu, name='havadurumu'),  # Hava durumu
    path('spor/', views.spor, name='spor'),  # Spor haberleri
    path('teknoloji/', views.teknoloji, name='teknoloji'),  # Teknoloji haberleri
]
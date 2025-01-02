from django.shortcuts import render
from .utils import get_collection_handle
from datetime import datetime
import pytz
from .models import News  # Haber modelinizi buraya ekleyin
import requests
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
import json

def home(request):
    collection, client = get_collection_handle('sondakika')
    news = []
    
    if collection is not None:
        try:
            news = list(collection.find().sort('published_date', -1).limit(24))
            
            seen_links = set()
            unique_news = []
            
            for item in news:
                if item['link'] not in seen_links:
                    seen_links.add(item['link'])
                    unique_news.append(item)
            
            news = unique_news
            
        except Exception as e:
            print(f"Haber çekme hatası: {e}")
        finally:
            if client:
                client.close()
    
    return render(request, 'news/home.html', {'news': news})

def category(request, category):
    collection, client = get_collection_handle(category)
    news = []
    
    if collection is not None:
        try:
            news = list(collection.find().sort('published_date', -1))
            
            seen_links = set()
            unique_news = []
            
            for item in news:
                if item['link'] not in seen_links:
                    seen_links.add(item['link'])
                    unique_news.append(item)
            
            news = unique_news
            
        except Exception as e:
            print(f"Kategori haberleri çekme hatası: {e}")
        finally:
            if client:
                client.close()
    
    return render(request, 'news/category.html', {
        'news': news,
        'category': category
    })

def search(request):
    query = request.GET.get('q', '')
    if query:
        # Başlık veya içerikte arama yap
        news_list = News.objects.filter(
            Q(title__icontains=query) |  # Başlıkta ara
            Q(content__icontains=query)   # İçerikte ara
        ).order_by('-created_at')  # En yeni haberler önce
    else:
        news_list = News.objects.none()  # Boş sorgu

    context = {
        'news_list': news_list,
        'query': query,
    }
    return render(request, 'news/search_results.html', context)

def fetch_weather_data():
    api_key = settings.OPENWEATHER_API_KEY
    cities = [
        'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Amasya', 'Ankara', 'Antalya', 'Artvin', 
        'Aydın', 'Balıkesir', 'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale',
        'Çankırı', 'Çorum', 'Denizli', 'Diyarbakır', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum',
        'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari', 'Hatay', 'Isparta', 'Mersin',
        'Istanbul', 'Izmir', 'Kars', 'Kastamonu', 'Kayseri', 'Kırklareli', 'Kırşehir', 'Kocaeli',
        'Konya', 'Kütahya', 'Malatya', 'Manisa', 'Kahramanmaraş', 'Mardin', 'Muğla', 'Muş', 'Nevşehir',
        'Niğde', 'Ordu', 'Rize', 'Sakarya', 'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Tekirdağ', 'Tokat',
        'Trabzon', 'Tunceli', 'Şanlıurfa', 'Uşak', 'Van', 'Yozgat', 'Zonguldak', 'Aksaray', 'Bayburt',
        'Karaman', 'Kırıkkale', 'Batman', 'Şırnak', 'Bartın', 'Ardahan', 'Iğdır', 'Yalova', 'Karabük',
        'Kilis', 'Osmaniye', 'Düzce'
    ]
    
    weather_data = []
    
    for city in cities:
        try:
            # Cache anahtarı oluştur
            cache_key = f'weather_{city.lower()}'
            # Önce cache'den veriyi kontrol et
            cached_data = cache.get(cache_key)
            
            if cached_data:
                weather_data.append(cached_data)
                continue
                
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city},TR&appid={api_key}&units=metric&lang=tr'
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_info = {
                    'city': city,
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': round(data['wind']['speed']),
                    'feels_like': round(data['main']['feels_like'])
                }
                # Her şehir için ayrı cache
                cache.set(cache_key, weather_info, 30 * 60)  # 30 dakika cache
                weather_data.append(weather_info)
                
        except Exception as e:
            print(f"Error fetching weather for {city}: {str(e)}")
            continue
    
    return weather_data

def weather_view(request):
    # Cache'den veriyi kontrol et
    cache_key = 'weather_data'
    weather_data = cache.get(cache_key)
    
    if weather_data is None:
        # Cache'de veri yoksa API'den çek
        weather_data = fetch_weather_data()
        
        # Veriyi 30 dakika boyunca cache'de tut
        if weather_data:  # Eğer veri başarıyla çekildiyse
            cache.set(cache_key, weather_data, 30 * 60)
    
    return render(request, 'news/weather.html', {'weather_data': weather_data})
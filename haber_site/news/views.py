from django.shortcuts import render
from .utils import get_collection_handle
from datetime import datetime
import pytz
from .models import News  # Haber modelinizi buraya ekleyin
import requests
from django.db.models import Q

def home(request):
    collection, client = get_collection_handle('sondakika')
    news = []
    
    if collection is not None:
        try:
            news = list(collection.find().sort('published_date', -1).limit(10))
            
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

def weather(request):
    api_key = "b3c53f46a07d0384f764935799a0b710"
    turkey_cities = [
        "Adana", "Adıyaman", "Afyonkarahisar", "Agrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin",
        "Aydin", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
        "Bursa", "Canakkale", "Cankiri", "Corum", "Denizli", "Diyarbakir", "Duzce", "Edirne", "Elazig", "Erzincan",
        "Erzurum", "Eskisehir", "Gaziantep", "Giresun", "Gumushane", "Hakkari", "Hatay", "Igdir", "Isparta", "Istanbul",
        "Izmir", "Kahramanmaras", "Karabuk", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kirikkale", "Kirklareli",
        "Kirsehir", "Kilis", "Kocaeli", "Konya", "Kutahya", "Malatya", "Manisa", "Mardin", "Mersin", "Mugla", "Mus",
        "Nevsehir", "Nigde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Sanliurfa",
        "Sirnak", "Tekirdag", "Tokat", "Trabzon", "Tunceli", "Usak", "Van", "Yalova", "Yozgat", "Zonguldak"
    ]
    
    weather_data = []
    
    for city in turkey_cities:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},TR&appid={api_key}&units=metric&lang=tr"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'city': city,
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s'yi km/h'ye çeviriyoruz
                    'feels_like': round(data['main']['feels_like'])
                }
                weather_data.append(weather_info)
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
            continue
    
    # Şehirleri alfabetik olarak sırala
    weather_data = sorted(weather_data, key=lambda x: x['city'])
    
    return render(request, 'news/weather.html', {'weather_data': weather_data})
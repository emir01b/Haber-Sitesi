# mongodb_app/views.py
from django.shortcuts import render
from .models import Category, Document, Sondakika

def index(request):
    son_dakika_haberleri = Sondakika.objects.all()
    context = {'son_dakika_haberleri': son_dakika_haberleri}
    return render(request, 'mongodb_app/index.html', context)

def dunya(request):
    dunya_haberleri = Document.objects.filter(category__name='Dünya')
    context = {'dunya_haberleri': dunya_haberleri}
    return render(request, 'mongodb_app/dunya.html', context)

def ekonomi(request):
    ekonomi_haberleri = Document.objects.filter(category__name='Ekonomi')
    context = {'ekonomi_haberleri': ekonomi_haberleri}
    return render(request, 'mongodb_app/ekonomi.html', context)

def spor(request):
    spor_haberleri = Document.objects.filter(category__name='Spor')
    context = {'spor_haberleri': spor_haberleri}
    return render(request, 'mongodb_app/spor.html', context)

def teknoloji(request):
    teknoloji_haberleri = Document.objects.filter(category__name='Teknoloji')
    context = {'teknoloji_haberleri': teknoloji_haberleri}
    return render(request, 'mongodb_app/teknoloji.html', context)

def havadurumu(request):
    # Hava durumu verilerini buradan alabilirsiniz
    # Örnek olarak, sabit veriler kullanabilirsiniz
    hava_durumu = {
        'İstanbul': {'temperature': '8°C', 'humidity': '53%', 'wind': '4 km/s'},
        'Ankara': {'temperature': '5°C', 'humidity': '45%', 'wind': '3 km/s'},
        'İzmir': {'temperature': '10°C', 'humidity': '60%', 'wind': '5 km/s'},
        'Bursa': {'temperature': '7°C', 'humidity': '50%', 'wind': '2 km/s'},
        'Antalya': {'temperature': '12°C', 'humidity': '70%', 'wind': '6 km/s'},
    }
    context = {'hava_durumu': hava_durumu}
    return render(request, 'mongodb_app/havadurumu.html', context)
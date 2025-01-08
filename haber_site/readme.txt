python manage.py run_news_fetcher
brew services start redis
python manage.py runserver

komutları ile projenin tüm fonkaiyonları aktif ve hızlı hale geliyor.
Hava durumu ilk açılışta bir tık geç yükleniyor fakat sonrasında veriler cache'de tutuluyor. 
Bu sayede çok daha hızlı yükleniyor.

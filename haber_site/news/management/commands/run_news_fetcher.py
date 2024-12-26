from django.core.management.base import BaseCommand
import feedparser
from datetime import datetime
import pytz
from time import mktime
from news.utils import get_collection_handle
import logging
import time
from django.utils import timezone
import requests

logger = logging.getLogger('news.fetcher')

class Command(BaseCommand):
    help = 'Sürekli olarak haber çekme işlemini gerçekleştirir'

    def fetch_news(self):
        RSS_FEEDS = {
            'sondakika': 'https://www.trthaber.com/sondakika_articles.rss',
            'dunya': 'https://www.trthaber.com/dunya_articles.rss',
            'ekonomi': 'https://www.trthaber.com/ekonomi_articles.rss',
            'spor': 'https://www.trthaber.com/spor_articles.rss',
            'bilim': 'https://www.trthaber.com/bilim_teknoloji_articles.rss'
        }

        current_time = timezone.localtime(timezone.now())
        self.stdout.write(f"Haber çekme görevi başladı - {current_time.strftime('%d-%m-%Y %H:%M:%S')}")
        turkey_tz = pytz.timezone('Europe/Istanbul')
        
        for category, url in RSS_FEEDS.items():
            try:
                self.stdout.write(f"{category} kategorisi için RSS feed'i okunuyor: {url}")
                
                # RSS feed'ini kontrol et
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"{category} RSS feed'i erişilemez: {response.status_code}"))
                    continue

                feed = feedparser.parse(url)
                
                if not feed.entries:
                    self.stdout.write(self.style.WARNING(f"{category} için haber bulunamadı!"))
                    continue
                    
                self.stdout.write(f"{category} için {len(feed.entries)} haber bulundu")
                
                collection, client = get_collection_handle(category)
                
                if collection is not None:
                    news_count = 0
                    for entry in feed.entries:
                        try:
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                                dt = pytz.UTC.localize(dt)
                                published_date = dt.astimezone(turkey_tz)
                            else:
                                published_date = datetime.now(turkey_tz)

                            # Haber içeriğini kontrol et
                            if not entry.title or not entry.link:
                                self.stdout.write(self.style.WARNING(f"Eksik veri: {entry}"))
                                continue

                            news_item = {
                                'title': entry.title,
                                'link': entry.link,
                                'description': getattr(entry, 'description', ''),
                                'published_date': published_date,
                                'image_url': entry.get('media_content', [{}])[0].get('url', '') 
                                           if 'media_content' in entry else '',
                                'category': category
                            }
                            
                            # Son dakika kategorisi için özel kontrol
                            if category == 'sondakika':
                                news_item['priority'] = True
                                # Son 24 saat kontrolü
                                if (timezone.now() - published_date).total_seconds() > 86400:
                                    continue
                            
                            result = collection.update_one(
                                {'link': entry.link},
                                {'$set': news_item},
                                upsert=True
                            )
                            
                            if result.modified_count > 0 or result.upserted_id:
                                news_count += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f"Yeni haber eklendi ({category}): {news_item['title']}")
                                )
                            
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f"Haber işlenirken hata: {str(e)}")
                            )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"{category} kategorisinde {news_count} yeni haber eklendi")
                    )
                    
                    if client:
                        client.close()
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"{category} kategorisi için hata oluştu: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Haber güncelleme görevi tamamlandı - {timezone.localtime(timezone.now()).strftime('%d-%m-%Y %H:%M:%S')}")
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Haber çekme servisi başlatıldı...'))
        
        while True:
            try:
                self.fetch_news()
                self.stdout.write('5 dakika bekleniyor...')
                time.sleep(300)  # 5 dakika bekle
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('\nServis durduruldu.'))
                break
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Beklenmeyen hata: {str(e)}. 5 dakika sonra tekrar denenecek...')
                )
                time.sleep(300) 
import feedparser
from datetime import datetime
from .utils import get_collection_handle
import pytz
from time import mktime

RSS_FEEDS = {
    'sondakika': 'https://www.trthaber.com/sondakika_articles.rss',
    'dunya': 'https://www.trthaber.com/dunya_articles.rss',
    'ekonomi': 'https://www.trthaber.com/ekonomi_articles.rss',
    'spor': 'https://www.trthaber.com/spor_articles.rss',
    'bilim': 'https://www.trthaber.com/bilim_teknoloji_articles.rss'
}

def fetch_news():
    turkey_tz = pytz.timezone('Europe/Istanbul')
    
    for category, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            collection, client = get_collection_handle(category)
            
            if collection is not None:
                for entry in feed.entries:
                    try:
                        # Tarih bilgisini al ve işle
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            # struct_time'ı datetime'a çevir
                            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
                            # UTC olarak işaretle
                            dt = pytz.UTC.localize(dt)
                            # Türkiye saatine çevir
                            published_date = dt.astimezone(turkey_tz)
                        else:
                            # Eğer tarih parse edilemezse şu anki zamanı kullan
                            published_date = datetime.now(turkey_tz)

                        news_item = {
                            'title': entry.title,
                            'link': entry.link,
                            'description': entry.description,
                            'published_date': published_date,
                            'image_url': entry.get('media_content', [{}])[0].get('url', '') 
                                       if 'media_content' in entry else '',
                            'category': category
                        }
                        
                        # MongoDB'ye kaydet
                        result = collection.update_one(
                            {'link': entry.link},
                            {'$set': news_item},
                            upsert=True
                        )
                        
                    except Exception as e:
                        print(f"Haber işlenirken hata: {e}")
                
                if client:
                    client.close()
                    
        except Exception as e:
            print(f"{category} kategorisi için hata oluştu: {e}")

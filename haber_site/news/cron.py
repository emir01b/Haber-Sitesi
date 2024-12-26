import feedparser
from datetime import datetime
import pytz
from time import mktime
from .utils import get_collection_handle
import logging

logger = logging.getLogger('news.cron')

def fetch_news():
    RSS_FEEDS = {
        'sondakika': 'https://www.trthaber.com/son-dakika.rss',
        'dunya': 'https://www.trthaber.com/dunya_articles.rss',
        'ekonomi': 'https://www.trthaber.com/ekonomi_articles.rss',
        'spor': 'https://www.trthaber.com/spor_articles.rss',
        'bilim': 'https://www.trthaber.com/bilim_teknoloji_articles.rss'
    }

    logger.info("Haber çekme görevi başladı - " + str(datetime.now()))
    turkey_tz = pytz.timezone('Europe/Istanbul')
    
    for category, url in RSS_FEEDS.items():
        try:
            logger.info(f"{category} kategorisi için RSS feed'i okunuyor")
            feed = feedparser.parse(url)
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

                        news_item = {
                            'title': entry.title,
                            'link': entry.link,
                            'description': entry.description,
                            'published_date': published_date,
                            'image_url': entry.get('media_content', [{}])[0].get('url', '') 
                                       if 'media_content' in entry else '',
                            'category': category
                        }
                        
                        result = collection.update_one(
                            {'link': entry.link},
                            {'$set': news_item},
                            upsert=True
                        )
                        
                        if result.modified_count > 0 or result.upserted_id:
                            news_count += 1
                            logger.info(f"Yeni haber eklendi: {news_item['title']}")
                        
                    except Exception as e:
                        logger.error(f"Haber işlenirken hata: {e}")
                
                logger.info(f"{category} kategorisinde {news_count} yeni haber eklendi")
                
                if client:
                    client.close()
                    
        except Exception as e:
            logger.error(f"{category} kategorisi için hata oluştu: {e}")

    logger.info("Haber güncelleme görevi tamamlandı - " + str(datetime.now())) 
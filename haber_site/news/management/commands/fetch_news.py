from django.core.management.base import BaseCommand
from news.tasks import fetch_news

class Command(BaseCommand):
    help = 'Fetch news from RSS feeds'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching news...')
        fetch_news()
        self.stdout.write(self.style.SUCCESS('Successfully fetched news'))

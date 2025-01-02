from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_hours(time_str, hours):
    try:
        # Saat:dakika formatındaki string'i datetime nesnesine çevir
        time = datetime.strptime(time_str, '%H:%M')
        # Saat ekle
        new_time = time + timedelta(hours=int(hours))
        # Tekrar string formatına çevir
        return new_time.strftime('%H:%M')
    except:
        return time_str 
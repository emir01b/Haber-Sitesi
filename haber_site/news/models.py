from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    # Diğer alanlar...

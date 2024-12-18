from django.db import models
from djongo import models  # MongoDB için djongo kullanıyorsanız

class Category(models.Model):
    name = models.CharField(max_length=100)

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Sondakika(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        db_table = 'sondakika'  # Koleksiyon adını burada belirtebilirsiniz

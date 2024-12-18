# mongodb_app/admin.py
from django.contrib import admin
from .models import Category, Document

admin.site.register(Category)
admin.site.register(Document)

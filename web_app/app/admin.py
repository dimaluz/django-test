from django.contrib import admin

from .models import Product, Tariff, Promotion

admin.site.register(Product)
admin.site.register(Tariff)
admin.site.register(Promotion)
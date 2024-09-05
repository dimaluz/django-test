from django.db import models
from django.core.validators import MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class Tariff(models.Model):
    product = models.ForeignKey(Product, related_name='tariff', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Promotion(models.Model):
    tariffs = models.ManyToManyField(Tariff, related_name='promotion')
    discount_name = models.CharField(max_length=250)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    date_discount_start = models.DateTimeField()
    date_discount_end = models.DateTimeField()

    def __str__(self):
        return self.discount_name

from django.test import TestCase
from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product, Tariff, Promotion

#Тесты для моделей

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product A')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Product A')


class TariffModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product A')
        self.tariff = Tariff.objects.create(name='Tariff A', price_base=Decimal('100.00'), product=self.product)

    def test_tariff_creation(self):
        self.assertEqual(self.tariff.name, 'Tariff A')
        self.assertEqual(self.tariff.price_base, Decimal('100.00'))
        self.assertEqual(self.tariff.product, self.product)


class PromotionModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product A')
        self.tariff = Tariff.objects.create(name='Tariff A', price_base=Decimal('100.00'), product=self.product)
        self.promotion = Promotion.objects.create(
            discount_name='Promo A',
            discount_percent=Decimal('20.00'),
            date_discount_start=datetime.now(),
            date_discount_end=datetime.now() + timedelta(days=10)
        )
        self.promotion.tariffs.add(self.tariff)

    def test_promotion_creation(self):
        self.assertEqual(self.promotion.discount_name, 'Promo A')
        self.assertEqual(self.promotion.discount_percent, Decimal('20.00'))
        self.assertIn(self.tariff, self.promotion.tariffs.all())


#Тестирование логики выборки акций

class PromotionDiscountTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product B')
        self.tariff = Tariff.objects.create(name='Tariff C', price_base=Decimal('200.00'), product=self.product)

        self.promo1 = Promotion.objects.create(
            discount_name='Promo B1',
            discount_percent=Decimal('10.00'),
            date_discount_start=datetime.now(),
            date_discount_end=datetime.now() + timedelta(days=5)
        )
        self.promo2 = Promotion.objects.create(
            discount_name='Promo B2',
            discount_percent=Decimal('20.00'),
            date_discount_start=datetime.now(),
            date_discount_end=datetime.now() + timedelta(days=10)
        )

        self.promo1.tariffs.add(self.tariff)
        self.promo2.tariffs.add(self.tariff)

    def test_best_promotion(self):
        tariff = Tariff.objects.get(name='Tariff C')
        best_promotion = tariff.promotion.order_by('-discount_percent').first()
        self.assertEqual(best_promotion.discount_name, 'Promo B2')
        self.assertEqual(best_promotion.discount_percent, Decimal('20.00'))

from rest_framework import serializers
from decimal import Decimal

from .models import Product 

class ProductXMLSerializer(serializers.ModelSerializer):
    tariffs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'tariffs']

    def get_tariffs(self, obj):
        tariffs_data = []
        for tariff in obj.tariff.all():
            promotion = tariff.promotion.order_by('-discount_percent').first()
            
            if promotion:
                price_with_discount = tariff.price_base * (Decimal(1) - (promotion.discount_percent / Decimal(100)))
            else:
                price_with_discount = tariff.price_base

            tariff_data = {
                'name': tariff.name,
                'price_base': tariff.price_base,
                'promotion': {
                    'discount_name': promotion.discount_name if promotion else None,
                    'discount_percent': promotion.discount_percent if promotion else None,
                    'date_discount_end': promotion.date_discount_end if promotion else None,
                    'price_with_discount': price_with_discount if promotion else None,
                }
            }

            tariffs_data.append(tariff_data)

        return tariffs_data
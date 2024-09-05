from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from django.db.models import Prefetch, OuterRef, Subquery
from django.utils.timezone import now


from .models import Product, Tariff, Promotion
from .serializers import ProductXMLSerializer

class ProductTariffView(APIView):
    renderer_classes = [XMLRenderer]

    def get(self, request):
        # Подзапрос для нахождения акции с максимальной скидкой для каждого тарифа
        best_promotion_subquery = Promotion.objects.filter(
            tariffs=OuterRef('pk'),
            date_discount_start__lte=now(),
            date_discount_end__gte=now()
        ).order_by('-discount_percent').values('id')[:1]

        # Используем Prefetch для предварительной загрузки акций с подзапросом
        tariffs_with_promotions = Tariff.objects.prefetch_related(
            Prefetch(
                'promotion',
                queryset=Promotion.objects.filter(
                    id__in=Subquery(best_promotion_subquery)
                )
            )
        )

        # Применяем prefetch_related для продукта
        products = Product.objects.prefetch_related(
            Prefetch('tariff', queryset=tariffs_with_promotions)
        )

        serializer = ProductXMLSerializer(products, many=True)
        return Response(serializer.data)



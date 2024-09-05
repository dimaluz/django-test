from django.urls import path

from .views import ProductTariffView

app_name = 'app'

urlpatterns = [
    path('products/', ProductTariffView.as_view(), name='products'),
]
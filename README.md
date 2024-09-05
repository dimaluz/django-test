# Django Products View

## Описание проекта

Этот проект реализует API для управления продуктами, тарифами и акциями. Он создан с использованием Django и Django Rest Framework и включает следующие ключевые модели:

- **Product**: содержит информацию о продуктах.
- **Tariff**: содержит информацию о тарифах, связанных с продуктами, включая базовую цену.
- **Promotion**: акции, которые применяются к тарифам и могут включать скидки с указанием периода действия.

## Модели

- **Product**
  - `name` (CharField): Название продукта.

- **Tariff**
  - `name` (CharField): Название тарифа.
  - `price_base` (DecimalField): Базовая цена тарифа.
  - `product` (ForeignKey): Ссылка на продукт.

- **Promotion**
  - `discount_name` (CharField): Название скидки.
  - `discount_percent` (DecimalField): Процент скидки.
  - `date_discount_start` (DateTimeField): Дата начала действия скидки.
  - `date_discount_end` (DateTimeField): Дата окончания действия скидки.
  - `tariff` (ManyToManyField): Список тарифов, к которым применяется акция.

## API

API предоставляет возможность получения данных о продуктах вместе с тарифами и активными акциями в формате XML.

### Пример XML ответа:

```xml
<root>
    <list-item>
    <name>Product_1</name>
    <tariffs>
        <list-item>
            <name>tariff_1</name>
            <price_base>100.00</price_base>
            <promotion>
                <discount_name>discount_1</discount_name>
                <discount_percent>20</discount_percent>
                <date_discount_end>2024-09-30 00:00:00+00:00</date_discount_end>
                <price_with_discount>80.000</price_with_discount>
            </promotion>
        </list-item>
    </tariffs>
    </list-item>
</root>
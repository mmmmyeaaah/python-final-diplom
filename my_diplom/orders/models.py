from django.db import models
from my_diplom import settings
from shops.models import ProductInfo
from users.models import Contact


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('assembled', 'Собран'),
        ('sent', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
        ('basket', "Статус корзины")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        related_name='my_diplom',
        on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        max_length=15,
        default='new'
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='Контакт',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']

    def __str__(self):
        return f'{self.state} {str(self.dt)}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Продукты',
        related_name='order_items',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1
    )

    def get_products(self):
        product_list = [product.name for product in self.product_info.all()]
        return ', '.join(product_list)

    get_products.short_description = 'Продукты'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Список заказанных товаров'
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
        ]

    def __str__(self):
        return self.order

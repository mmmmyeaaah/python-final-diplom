from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Shop(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название магазина'
    )
    url = models.URLField(
        verbose_name='Ссылка',
        null=True,
        blank=True
    )
    filename = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    state = models.BooleanField(verbose_name='статус получения заказов', default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        ordering = ['-name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории'
    )
    shops = models.ManyToManyField(
        Shop,
        verbose_name='Магазины',
        related_name='categories',
        blank=True
    )

    def get_shops(self):
        shop_list = [shop.name for shop in self.shops.all()]
        return ', '.join(shop_list)

    get_shops.short_description = 'Магазины'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название продукта'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        related_name='products',
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-name']

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Модель'
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость'
    )
    price_rrc = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Рекомендуемая цена'
    )
    product = models.ForeignKey(
        Product, verbose_name='Продукты',
        related_name='product_info',
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop, verbose_name='Магазин',
        related_name='product_info',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информация о продуктах, остатки'
        ordering = ['-name']
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_info'),
        ]

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список имен параметров"
        ordering = ['-name']

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Информация о продукте',
        related_name='product_parameters',
        blank=True,
        on_delete=models.CASCADE
    )
    parameter = models.ForeignKey(
        Parameter,
        verbose_name='Параметр',
        related_name='product_parameters',
        blank=True,
        on_delete=models.CASCADE
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=50
    )

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]


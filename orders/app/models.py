from fileinput import filename

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        # ordering = ['date_joined']


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название магазина')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    filename = models.CharField(max_length=50, blank=True) # что это????????

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ['-name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    shops = models.ManyToManyField(
        Shop, verbose_name='Магазины',
        related_name='categories', blank=True
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
    name = models.CharField(max_length=50, verbose_name='Название продукта')
    category = models.ForeignKey(
        Category, verbose_name='Категории',
        related_name='products', blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-name']

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Товар')
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
        # constraints = [
        #     models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_info'),
        # ]

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

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
        related_name='product_info',
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
    value = models.CharField(verbose_name='Значение', max_length=50)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"
        # constraints = [
        #     models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        # ]


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('assembled', 'Собран'),
        ('sent', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    )
    user = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='orders',
        on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус заказа', choices=STATUS_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ['-dt']

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name='Заказ',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    product = models.ManyToManyField(
        Product, verbose_name='Продукты',
        related_name='order_items',
    )
    shop = models.ManyToManyField(
        Shop, verbose_name='Магазин',
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Список заказанных товаров'
        # constraints = [
        #     models.UniqueConstraint(fields=['order_id',], name='unique_order_item'),
        # ]


class Contact(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Контакт',
        related_name='contact',
        on_delete=models.CASCADE
    )
    # value = ...
    # type = ...
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=50, verbose_name='Дом')
    apartment = models.CharField(max_length=50, verbose_name='Квартира')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = 'Список контактов пользователей'
        
    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment}'

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django_rest_passwordreset.tokens import get_token_generator

from orders import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('shop', 'Магазин'),
        ('buyer', 'Покупатель'),
    )
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    type = models.CharField(
        verbose_name='Тип пользователя',
        choices=USER_TYPE_CHOICES,
        max_length=5,
        default='buyer'
    )
    is_active = models.BooleanField(
        verbose_name='Пользователь активен',
        default=False
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"


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
    filename = models.CharField(max_length=50, blank=True) # что это????????
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


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        related_name='contact',
        on_delete=models.CASCADE
    )
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=50, verbose_name='Дом')
    apartment = models.CharField(max_length=50, verbose_name='Квартира')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = 'Контакты пользователей'

    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment}'


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
        related_name='orders',
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
        Product,
        verbose_name='Продукты',
        related_name='order_items',
        on_delete=models.CASCADE,
        blank=True, null=True
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


class ConfirmEmailToken(models.Model):
    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name='Юзер, которому пренадлежит токен'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата генерации токена'
    )

    key = models.CharField(
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)

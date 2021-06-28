from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from .choices import *

User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Зображення')
    description = models.TextField(verbose_name='Опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')
    for_main_page = models.BooleanField(default=False, verbose_name='Показувати на головній')
    # основні характеристики
    conditioner_type = models.CharField(max_length=255, verbose_name='Тип кондиціонера', choices=CONDITIONER_TYPE_CHOICES, null=True, blank=True)
    brand = models.CharField(max_length=255, choices=BRAND_CHOICES, verbose_name='Бренд', null=True, blank=True)
    cold_efficiency = models.CharField(max_length=255, verbose_name='Продуктивність холод, кВт', null=True, blank=True)
    warm_efficiency = models.CharField(max_length=255, verbose_name='Продуктивність тепло, кВт', null=True, blank=True)
    cold_watt_consumption = models.CharField(max_length=255, verbose_name='Споживання потужності холод, кВт', null=True, blank=True)
    warm_watt_consumption = models.CharField(max_length=255, verbose_name='Споживання потужності тепло, кВт', null=True, blank=True)
    recommended_area = models.CharField(max_length=255, verbose_name='Рекомендована площа приміщення, м²', choices=AREA_CHOICES, null=True, blank=True)
    invertor = models.CharField(max_length=255, verbose_name='Інвертор', choices=INVERTOR_CHOICES, null=True, blank=True)
    energy_efficiency = models.CharField(max_length=255, verbose_name='Енергоефективність EER/C.O.P.,кВт/кВт', null=True, blank=True)
    liquid_tube_diameter = models.CharField(max_length=255, verbose_name='Діаметер рідинної труби, мм', null=True, blank=True)
    gas_tube_diameter = models.CharField(max_length=255, verbose_name='Діаметер газової труби, мм', null=True, blank=True)
    max_magistral_length = models.PositiveIntegerField(verbose_name='Максимальна довжина магістралі, м', null=True, blank=True)
    max_magistral_hight_variation = models.PositiveIntegerField(verbose_name='Максимальний перепад висоти магістралі, м', null=True, blank=True)
    cold_work_temratures = models.CharField(max_length=255, verbose_name='Діапазон роботи на холод,°C', null=True, blank=True)
    warm_work_temratures = models.CharField(max_length=255, verbose_name='Діапазон роботи на тепло,°C', null=True, blank=True)
    freon = models.CharField(max_length=255, verbose_name='Фреон', null=True, blank=True)
    energy_source = models.CharField(max_length=255, verbose_name='Джерело живлення', null=True, blank=True)
    warrant = models.CharField(max_length=255, verbose_name='Гарантія', null=True, blank=True)
    manufacturer = models.CharField(max_length=255, verbose_name='Виробник', null=True, blank=True)
    # внутрішній блок
    dims = models.CharField(max_length=255, verbose_name='Габаритні розміри, мм', null=True, blank=True)
    weight = models.CharField(max_length=255, verbose_name='Вага, кг', null=True, blank=True)
    noise = models.CharField(max_length=255, verbose_name='Рівень шуму,дБ(А)(мин/ср/макс)', null=True, blank=True)
    air_consumption = models.CharField(max_length=255, verbose_name='Споживання повітря, м³/год.', null=True, blank=True)
    filter = models.CharField(max_length=255, verbose_name='Фільтр', null=True, blank=True)
    color = models.CharField(max_length=255, verbose_name='Колір', null=True, blank=True)
    # зовнішній блок
    outer_dims = models.CharField(max_length=255, verbose_name='Габаритні розміри, мм', null=True, blank=True)
    outer_weight = models.CharField(max_length=255, verbose_name='Вага, кг', null=True, blank=True)
    outer_noise = models.CharField(max_length=255, verbose_name='Рівень шуму,дБ(А)(мин/ср/макс)', null=True, blank=True)
    outer_distance_between_bases = models.CharField(max_length=255, verbose_name='Відстань між лапами, мм', null=True, blank=True)
    compressor_type = models.CharField(max_length=255, verbose_name='Тип компресора', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна ціна')

    def __str__(self):
        return "Продукт: {} (для корзини)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Загальна цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефону', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_order')

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення обробляється'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупець', related_name='related_orders', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментар до замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')
    order_date = models.DateField(verbose_name='Дата отримання замовлення', default=timezone.now)

    def __str__(self):
        return str(self.id)


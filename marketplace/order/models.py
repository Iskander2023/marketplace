from django.db import models
from order import settings
from catalog.models import Product
from app_profile.models import Profile


class Order(models.Model):
    """
    Модель заказа
    """
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='пользователь', related_name='orders')
    deliveryType = models.CharField(max_length=128, default=settings.deliveryType[0], verbose_name='тип доставки')
    paymentType = models.CharField(max_length=128, default=settings.paymentType[0], verbose_name='тип оплаты')
    totalCost = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='сумма заказа')
    status = models.CharField(max_length=128, default=settings.status[0], verbose_name='статус')
    city = models.CharField(max_length=256, default='', verbose_name='город')
    address = models.CharField(max_length=256, default='', verbose_name='адрес')
    products = models.ManyToManyField(Product, related_name='orders', verbose_name='продукты')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def email(self):
        return self.user.email

    def fullName(self):
        return self.user.fullName

    def phone(self):
        return self.user.phone

    def orderId(self):
        return f'{self.pk}'

    def __str__(self):
        return f'{self.pk}'


class CountProductinOrder(models.Model):
    """
    Количество товаров в заказе
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
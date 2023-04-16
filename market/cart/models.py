from django.db import models
from shops.models import Offer
from users.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class Delivery(models.Model):
    """Доставка заказа."""
    DELIVERY_OPTIONS = (
        ('Delivery', 'Доставка'),
        ('Express Delivery', 'Экспресс-доставка'),
    )
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_OPTIONS, verbose_name=_('способ доставки'))
    express_delivery_fee = models.PositiveIntegerField(default=500, verbose_name=_('плата за экспресс доставку'))
    order_total_for_free_delivery = models.PositiveIntegerField(default=2000, verbose_name=_('минимальная стоимость заказа для бесплатной доставки'))
    delivery_fee = models.PositiveIntegerField(default=200, verbose_name=_('стоимость доставки'))

    def __str__(self):
        return f'{self.delivery_option} ({self.delivery_fee} руб.)'


class Order(models.Model):
    """Заказ пользователя сайта."""
    STATUS_CHOICES = (
        ('created', 'Создан'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Отменено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('пользователь'), blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('создано'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('обнавлено'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name=_('статус'))
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=_('дата оплаты'))
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name=_('способ доставки'))
    delivery_adress = models.CharField(max_length=100, verbose_name=_('адрес доставки'))
    offer = models.ManyToManyField(Offer, through='OrderItem')

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        if self.status == 'paid' and not self.payment_date:
            self.payment_date = datetime.now()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Элемент заказа."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('заказ'), related_name='items')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name=_('предложение'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('количество'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('дата добавления'))

    class Meta:
        verbose_name = _('позиция заказа')
        verbose_name_plural = _('позиции заказа')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.offer.price * self.quantity

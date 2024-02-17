from django.db import models

from user.models import User


# Create your models here.


class Order(models.Model):

    ORDER_STATUS = (
        (0, 'Досталвено'),
        (1, 'Отменен'),
        (2, 'Неоплачено'),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Покупатель')
    user_info = models.ForeignKey('UserInfo', null=True, on_delete=models.SET_NULL, verbose_name='Информация о доставке')
    basket = models.JSONField(verbose_name='Товары')
    status = models.CharField(choices=ORDER_STATUS, max_length=10, verbose_name='Статус заказа')
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')



class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    country = models.CharField(max_length=40, verbose_name='Страна')
    city = models.CharField(max_length=40, verbose_name='Город')
    street = models.CharField(max_length=40, verbose_name='Улица')
    postal_code = models.CharField(max_length=10, verbose_name='Почтовый индекс')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    email = models.CharField(max_length=50, verbose_name='Электронная почта')

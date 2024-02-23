from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from user.models import User


# Create your models here.


class Order(models.Model):

    ORDER_STATUS = (
        ('Досталвено', 'Досталвено'),
        ('Отменен', 'Отменен'),
        ('Неоплачено', 'Неоплачено'),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Покупатель')
    user_info = models.ForeignKey('UserInfo', null=True, on_delete=models.SET_NULL, verbose_name='Информация о доставке')
    basket = models.JSONField(verbose_name='Товары')
    status = models.CharField(choices=ORDER_STATUS, max_length=10, verbose_name='Статус заказа')
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is not None:
            old_order = Order.objects.get(pk=self.pk)
            if self.status != old_order.status:
                send_mail(f'Статус заказа {self.id} изменился',
                          f'Статус вашего заказа изменился на {self.status}',
                          settings.EMAIL_HOST_USER,
                          [f'{self.user.email}'],
                          fail_silently=False
                          )
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)




class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    country = models.CharField(max_length=40, verbose_name='Страна')
    city = models.CharField(max_length=40, verbose_name='Город')
    street = models.CharField(max_length=40, verbose_name='Улица')
    postal_code = models.CharField(max_length=10, verbose_name='Почтовый индекс')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона')
    email = models.CharField(max_length=50, verbose_name='Электронная почта')

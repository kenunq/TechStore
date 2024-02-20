from django.contrib import admin

from Orders.models import Order, UserInfo


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'order_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user_info__country', 'user_info__city')

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'street', 'postal_code', 'phone_number', 'email')
    search_fields = ('user__username', 'country', 'city')

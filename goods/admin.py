from django.contrib import admin

from goods.models import (
    ProductFeature,
    Product,
    Feature,
    ProductImage,
    Category,
    Basket,
)


# Register your models here.


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature


class ImageInline(admin.TabularInline):
    fk_name = "product"
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "available_quantity")
    search_fields = ("name", "brand")
    list_filter = ("category", "brand")
    inlines = [ProductFeatureInline, ImageInline]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    search_fields = ("product", "user")
    list_filter = ("product",)

from django.db import models

from user.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField("Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена товара")
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Устаревшая цена товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="a_category",
        verbose_name="Категория",
    )
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    available_quantity = models.PositiveIntegerField(default=0, verbose_name="Количество товара на складе")
    features = models.ManyToManyField("Feature", through="ProductFeature", verbose_name="Характеристики")
    is_published = models.BooleanField(default=False, verbose_name="Статус публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images", null=True, blank=True)

    def __str__(self):
        return f"Изображение для {self.product.name}"


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.feature.name}: {self.value}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Количество")

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Корзина {self.user}"

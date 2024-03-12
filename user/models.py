from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Имя")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    SEX = (("Женщина", "Женщина"), ("Мужчина", "Мужчина"), ("Другое", "Другое"))
    gender = models.CharField(max_length=7, choices=SEX, default=0, verbose_name="Пол")

    class Meta:
        verbose_name = "Пользователю"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.name:
            return self.name
        return self.username

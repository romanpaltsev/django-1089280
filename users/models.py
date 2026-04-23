from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", default="users/default.jpg", null=True, blank=True, verbose_name="Фото")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
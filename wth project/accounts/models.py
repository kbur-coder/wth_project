from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.get_full_name() or self.username
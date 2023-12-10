from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password')

    class Meta:
        db_table = "User"

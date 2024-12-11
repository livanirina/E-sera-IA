from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Modifier le related_name
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to.",
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Modifier le related_name
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
        related_query_name="customuser",
    )

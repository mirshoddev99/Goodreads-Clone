from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    password2 = models.CharField(max_length=255, blank=False, null=False)
    profile_picture = models.ImageField(default='default_pic.jpg')

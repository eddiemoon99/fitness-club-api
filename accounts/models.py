from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE

# extended user from base django model

class User(AbstractUser):
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  phone_number = models.CharField(max_length=200, default='xxx-xxx-xxxx')
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.username}"

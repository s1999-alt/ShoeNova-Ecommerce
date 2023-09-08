from django.db import models 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
User = get_user_model()

class Userprofile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
  name = models.CharField(max_length=255,default='')
  is_blocked = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.user.username




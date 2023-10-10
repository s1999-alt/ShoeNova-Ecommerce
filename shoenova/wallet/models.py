from django.db import models
from app.models import UserProfile


class Wallet(models.Model):
  user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
  balance = models.IntegerField(default=0)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.user.username + str(self.balance)
  

class WalletTransaction(models.Model):
  TRANSACTION_TYPE_CHOICES =(
    ("CREDIT", "Credit"),
    ("DEBIT", "Debit"),
  )
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=10)
  transaction_detail = models.CharField(max_length=50)
  amount = models.IntegerField(default=0)
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.transaction_type + str(self.wallet) + str(self.amount)


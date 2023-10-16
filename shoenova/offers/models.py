from django.db import models
from myapp.models import Product,Category

class ProductOffer(models.Model):
  offer_name = models.CharField(max_length=100)
  expire_date = models.DateField()
  product = models.ManyToManyField(Product)
  discount_percentage = models.IntegerField(default=0)
  product_offer_slug = models.SlugField(blank=True, max_length=200,unique=True)
  product_offer_images = models.ImageField(upload_to='photos/offerimages', null=True)
  is_active = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if self.discount_percentage > 100:
      self.discount_percentage = 100

  def __str__(self):
    return self.offer_name 




class CategoryOffer(models.Model):
  offer_name = models.CharField(max_length=100)
  expire_date = models.DateField()
  category = models.ManyToManyField(Category)
  discount_percentage = models.IntegerField(default=0)
  product_offer_slug = models.SlugField(blank=True, max_length=200,unique=True)
  product_offer_images = models.ImageField(upload_to='photos/offerimages', null=True)
  is_active = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if self.discount_percentage > 100:
      self.discount_percentage = 100

  def __str__(self):
    return self.offer_name        



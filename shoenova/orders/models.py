from django.db import models
from app.models import UserProfile
from myapp.models import Product,Variations




class PaymentMethod(models.Model):
   method_name = models.CharField(max_length=50)
   is_active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)



class Payment(models.Model):
  PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
      )
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  payment_id = models.CharField(max_length=100)
  payment_order_id = models.CharField(max_length=100,null=True,blank=True)
  payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
  amount_paid = models.CharField(max_length=100)#total amount paid
  status = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.payment_id
  

class Coupon(models.Model):
   coupon_code = models.CharField(max_length=50, unique=True)
   discount = models.DecimalField(max_digits=10, decimal_places=0)
   valid_from = models.DateTimeField()
   valid_to = models.DateTimeField()
   active = models.BooleanField(default=True)
   minimum_amount = models.IntegerField(default=500)

   def __str__(self):
       return self.coupon_code




class Order(models.Model):
  STATUS = (
    ('New','New'),
    ('Accepted','Accepted'),
    ('Completed','Completed'),
    ('Cancelled','Cancelled'),
  )

  user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
  payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
  coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, null=True)#NEED TO REMOVE THE NULL=TRUE WHENEVER I TRUNCATE THE DATABASE
  order_number = models.CharField(max_length=20)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone = models.CharField(max_length=15)
  email = models.EmailField(max_length=50)
  address_line_1 = models.CharField(max_length=50)
  address_line_2 = models.CharField(max_length=50, blank=True)
  country = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  pin_code = models.CharField(max_length=6,default=False)
  order_note = models.CharField(max_length=100, blank=True)
  order_total = models.FloatField()
  status = models.CharField(max_length=10, choices=STATUS, default='New')
  ip = models.CharField(blank=True, max_length=20)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def full_name(self):
     return f'{self.first_name} {self.last_name}'
  
  def full_address(self):
     return f'{self.address_line_1} {self.address_line_2}'

  def __str__(self):
      return self.first_name
  



class OrderProduct(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE)
   user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   variation = models.ManyToManyField(Variations)
   quantity = models.IntegerField()
   product_price = models.FloatField
   ordered =models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.product.product_name 
   


   


  




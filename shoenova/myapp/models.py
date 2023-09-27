from django.db import models
from django.utils.text import slugify
from app.models import UserProfile
from django.urls import reverse




class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20,unique=False)
    description = models.TextField(max_length=100,blank= True)
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    category_image = models.ImageField(upload_to='photos/categories',blank= True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)   
    

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200,blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    soft_deleted = models.BooleanField(default=False)
    product_images = models.ImageField(upload_to='photos/products',null=True)
    product_images2 = models.ImageField(upload_to='photos/products',null=True)
    product_images3 = models.ImageField(upload_to='photos/products',null=True)
    product_images4 = models.ImageField(upload_to='photos/products',null=True)
    product_images5 = models.ImageField(upload_to='photos/products',null=True)


    def get_url(self):
         return reverse('product-details', args=[self.id])
    

    def __str__(self):
           return self.product_name 
     
    

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete =models.CASCADE,null=True)


    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)  
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.DecimalField(max_digits=10,decimal_places=2, default=0)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product

    def sub_total(self):
        return self.product.price * self.quantity      





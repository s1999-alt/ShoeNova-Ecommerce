from django.contrib import admin
from .models import Payment, Order, OrderProduct, PaymentMethod


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(PaymentMethod)

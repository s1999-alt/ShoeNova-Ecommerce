from django.contrib import admin
from .models import Payment, Order, OrderProduct, PaymentMethod,Coupon


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(PaymentMethod)
admin.site.register(Coupon)

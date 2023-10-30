from django.contrib import admin

# Register your models here.
from .models import Category, Product, Cart, CartItem,Variations,Wishlist,Banner_area


class VariationAdmin(admin.ModelAdmin):
  list_display = ('product','variation_category','variation_value','is_active')
  list_editable = ('is_active',)
  list_filter = ('product','variation_category','variation_value')


class CartAdmin(admin.ModelAdmin):
  list_display = ('cart_id','date_added')


class CartItemAdmin(admin.ModelAdmin):
  list_display = ('product','cart','quantity','is_active')


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variations,VariationAdmin)
admin.site.register(Wishlist)
admin.site.register(Banner_area)
from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
  path('offers', views.offers, name='offers'),
  path('category-offer-product/<slug:offer_slug>', views.category_offer_product, name='category-offer-product'),
  path('product-offer-product/<slug:offer_slug>', views.product_offer_product, name='product-offer-product'),


  path('add-category-offer', views.add_category_offer, name='add-category-offer'),
  path('add-product-offer', views.add_product_offer, name='add-product-offer'),


]

from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
  path('admin-index/', views.adm_index, name='admin-index'),
  path('admn-product-list/', views.Admn_product_list, name='admn-product-list'),
    
]


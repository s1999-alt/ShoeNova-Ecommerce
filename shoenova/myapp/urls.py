from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
  path('admin-index/', views.adm_index, name='admin-index'),

  path('admn-product-list/', views.admn_product_list, name='admn-product-list'),
  path('admn_add_product/', views.admn_add_product, name='admn_add_product'),

  path('admn_product_category/', views.admn_product_category, name='admn_product_category'),
  path('admn_add_categories_page/', views.admn_add_categories_page, name='admn_add_categories_page'),
  path('admn_add_categories/', views.admn_add_categories, name='admn_add_categories'),

  path('admn_users_list/', views.admn_users_list, name='admn_users_list'),

    
]


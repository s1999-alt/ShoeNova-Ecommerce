from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
  path('admin-index/', views.adm_index, name='admin-index'),




  path('admn-product-list/', views.admn_product_list, name='admn-product-list'),
  path('admn_add_product/', views.admn_add_product, name='admn_add_product'),
  path('admn_edit_product/<int:id>/', views.admn_edit_product, name='admn_edit_product'),
  path('admn_delete_product/<int:id>', views.admn_delete_product, name='admn_delete_product'),



  path('admn_product_category/', views.admn_product_category, name='admn_product_category'),
  path('admn_add_categories/', views.admn_add_categories, name='admn_add_categories'),
  path('admn_enable_disable_categories/<int:id>', views.admn_enable_disable_categories, name='admn_enable_disable_categories'),
  path('admn_delete_categories/<int:id>', views.admn_delete_categories, name='admn_delete_categories'),
  path('admn_edit_categories/<int:id>', views.admn_edit_categories, name='admn_edit_categories'),

  path('admn_users_list/', views.admn_users_list, name='admn_users_list'),
  path('admn_users_block_unblock/<int:id>', views.admn_users_block_unblock, name='admn_users_block_unblock'),

    
]


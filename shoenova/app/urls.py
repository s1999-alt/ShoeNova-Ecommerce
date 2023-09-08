from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base_view, name='base'),
    path('login-register/', views.login_regis, name='login-register'),
    path('product-detail/', views.Admn_product_list, name='product-detail'),



   
    path('admin-index/', views.adm_index, name='admin-index'),
    path('admn-product-list/', views.Admn_product_list, name='admn-product-list'),



    

]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base_view, name='base'),
    path('login-register/', views.login_regis, name='login-register'),
    path('login-page/', views.login_page, name='login-page'),
    path('product-detail/', views.product_details, name='product-detail'),
   



   
   



    

]

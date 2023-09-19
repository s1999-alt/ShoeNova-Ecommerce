from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base_view, name='base'),
    path('login-register/', views.login_regis, name='login-register'),
    path('login-page/', views.login_page, name='login-page'),
    path('handlelogout/', views.handlelogout, name='handlelogout'),
    path('product-details/<int:id>/', views.product_details, name='product-details'),
    path('otp-regis/', views.otp_regis, name='otp-regis'),
    

]

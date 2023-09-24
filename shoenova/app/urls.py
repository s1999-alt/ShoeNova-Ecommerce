from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base_view, name='base'),
    path('login-register/', views.login_regis, name='login-register'),
    path('login-page/', views.login_page, name='login-page'),
    path('handlelogout/', views.handlelogout, name='handlelogout'),
    path('product-details/<int:id>/', views.product_details, name='product-details'),
    path('shop-product/', views.shop_product, name='shop-product'),
    path('shop/category/<slug:category_slug>/', views.shop_product_by_category, name='shop-product-by-category'),
    path('otp-regis/', views.otp_regis, name='otp-regis'),
    path('password-reset-request/', views.password_reset_request, name='password-reset-request'),
    path('forgot-password-otp/', views.forgot_password_otp, name='forgot-password-otp'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('password-reset-success/', views.password_reset_success, name='password-reset-success'),
    path('shop-cart/', views.shop_cart, name='shop-cart'),

    

]

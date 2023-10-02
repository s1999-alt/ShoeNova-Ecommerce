from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base_view, name='base'),
    path('login-register/', views.login_regis, name='login-register'),
    path('login-page/', views.login_page, name='login-page'),
    path('handlelogout/', views.handlelogout, name='handlelogout'),
    path('category/product-details/<int:id>/', views.product_details, name='product-details'),
    path('shop-product/', views.shop_product, name='shop-product'),
    path('shop/category/<slug:category_slug>/', views.shop_product_by_category, name='shop-product-by-category'),



    path('otp-regis/', views.otp_regis, name='otp-regis'),
    path('password-reset-request/', views.password_reset_request, name='password-reset-request'),
    path('forgot-password-otp/', views.forgot_password_otp, name='forgot-password-otp'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('password-reset-success/', views.password_reset_success, name='password-reset-success'),


    path('add-cart/<int:id>/', views.add_cart, name='add-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-cart/<int:id>/<int:cart_item_id>/', views.remove_cart, name='remove-cart'),#decrement one from quantity
    path('delete-cart/<int:id>/<int:cart_item_id>/', views.delete_cart, name='delete-cart'),


    path('search/', views.search, name='search'),


    path('checkout/', views.checkout, name='checkout'),


]

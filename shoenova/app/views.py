from django.shortcuts import render,redirect

# Create your views here.

#user
def index(request):
    return render(request,'user/index.html')

def base_view(request):
    return render(request, 'user/base.html')

def login_regis(request):
    return render(request, 'user/page-login-register.html')

def login_page(request):
    return render(request, 'user/page-login.html')

def product_details(request):
    return render(request, 'user/shop-product-left.html')




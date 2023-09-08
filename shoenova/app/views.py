from django.shortcuts import render,redirect

# Create your views here.

#user
def index(request):
    return render(request,'user/index.html')

def base_view(request):
    return render(request, 'user/base.html')

def login_regis(request):
    return render(request, 'user/page-login-register.html')

def product_details(request):
    return render(request, 'user/shop-product-left.html')


#admin
def adm_index(request):
    return render(request, 'admin/index.html')

def Admn_product_list(request):
    return render(request, 'page-products-list.html')
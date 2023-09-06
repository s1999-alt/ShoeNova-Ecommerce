from django.shortcuts import render,redirect

# Create your views here.

def index(request):
    return render(request,'user/index.html')

def base_view(request):
    return render(request, 'user/base.html')

def login_regis(request):
    return render(request, 'user/page-login-register.html')

def adm_index(request):
    return render(request, '')
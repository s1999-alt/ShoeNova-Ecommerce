from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

#user
def index(request):
    return render(request,'user/index.html')

def base_view(request):
    return render(request, 'user/base.html')

def login_regis(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirmpassword=request.POST.get("confirmpassword") 
        # print(username,email,password,confirmpassword)
        if password!=confirmpassword:
            messages.warning(request, "Password is Incorrect")
            return redirect('/login-register')
        try:
            if User.objects.get(username=username):
                return HttpResponse("Username Already Taken")
        except:
            pass
        try:
            if User.objects.get(email=email):
                return HttpResponse("Email is already taken")  
        except:
            pass      
        myuser=User.objects.create_user(username,email,password)
        myuser.save()
        return HttpResponse("Signup Successfully")
    return render(request, 'user/page-login-register.html')

def login_page(request):
    return render(request, 'user/page-login.html')

def product_details(request):
    return render(request, 'user/shop-product-left.html')




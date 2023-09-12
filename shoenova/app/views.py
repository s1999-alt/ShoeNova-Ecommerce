from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile

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
            if UserProfile.objects.filter(username=username).exists():
                messages.warning(request, "Username Is Already Taken")
                return redirect("/login-register")
        except:
            pass
        try:
            if UserProfile.objects.filter(email=email).exists():
                messages.info(request, "Email Is Already Taken")
                return redirect("/login-register")
        except:
            pass      
        myuser = UserProfile.objects.create_user(username=username, email=email, password=password)
        myuser.save()
        messages.success(request, "Signup Successfully..Please Login!")
        return redirect("/login-page")
    return render(request, 'user/page-login-register.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/') 
        else:
            messages.warning(request, "Invalid credentials. Please try again.")

    return render(request, 'user/page-login.html')
    

def product_details(request):
    return render(request, 'user/shop-product-left.html')




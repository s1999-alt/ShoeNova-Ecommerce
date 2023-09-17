from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from myapp.models import Product

# Create your views here.

#user

def index(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'user/index.html',context)

def base_view(request):
    return render(request, 'user/base.html')

def login_regis(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone") 
        password=request.POST.get("password")
        confirmpassword=request.POST.get("confirmpassword")
        
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
        myuser = UserProfile.objects.create_user(username=username, email=email, phone=phone, password=password)
        myuser.save()
        messages.success(request, "Signup Successfully..Please Login!")
        return redirect("/login-page")
    return render(request, 'user/page-login-register.html')



def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
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


@login_required(login_url='/login-page')
def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Succesfully")
    return redirect('/login-page')



    
def product_details(request):
    return render(request, 'user/shop-product-left.html')




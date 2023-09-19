from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myapp.models import Product
from .utils import send_otp
from datetime import datetime
import pyotp
# Create your views here.

#user


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'user/index.html',context)


def base_view(request):
    return render(request, 'user/base.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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
        myuser = UserProfile.objects.create_user(email=email, phone=phone, password=password)
        myuser.save()
        messages.success(request, "Signup Successfully..Please Login!")
        return redirect("/login-page")
    return render(request, 'user/page-login-register.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def otp_regis(request):
    if request.method=="POST":
        otp=request.POST['otp']
        email=request.session['email']

        otp_secret_key=request.session['otp_secret_key']
        otp_valid_until=request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until=datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp=pyotp.TOTP(otp_secret_key, interval=120)

                if totp.verify(otp):
                     user=get_object_or_404(UserProfile,email=email)
                     request.session['email_']=email
                     login(request, user)
                     del request.session['email']

                     del request.session['otp_secret_key']
                     del request.session['otp_valid_date']

                     return redirect('/')
                else:
                    messages.warning(request, 'Invalid One time Password')
            else:
                messages.warning(request,'One time password has Expired')
        else:
            messages.warning(request, 'oops...something went wrong')            

    return render(request, 'user/otp.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            send_otp(request, email)
            request.session['email'] = email
            return redirect('otp-regis')
            # login(request, user)
            # return redirect('/') 
        else:
            messages.warning(request, "Invalid credentials. Please try again.")

    return render(request, 'user/page-login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='/login-page')
def handlelogout(request):
    if 'email_' in request.session:
        del request.session['email_']
    logout(request)
    messages.info(request, "Logout Succesfully")
    return redirect('/login-page')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)   
def product_details(request, id):
    products=Product.objects.get(id=id)
    context={
        'products':products
    }
    return render(request, 'user/shop-product-details.html',context)

def shop_product(request):
    return render(request, 'user/page-shop.html')




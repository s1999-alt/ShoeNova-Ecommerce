from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myapp.models import Product,Category
from .utils import send_otp,resend_otp
from datetime import datetime
import pyotp
# Create your views here.

#user


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    context={
        'products':products,
        'categories':categories
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
        if 'otp_resend' in request.POST:  # Check if Resend OTP button was clicked
            resend_otp(request)
            return redirect('otp-regis')  # Redirect back to OTP page after resending

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
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            if email is not None:
                send_otp(request, email)
                request.session['email'] = email
                return redirect('forgot-password-otp')
        except UserProfile.DoesNotExist:
            messages.warning(request, "Invalid Email. Please Enter a Valid One.") 
    return render(request, 'password-reset-request.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def forgot_password_otp(request):
    if request.method=="POST":
        if 'otp_resend' in request.POST:  # Check if Resend OTP button was clicked
            resend_otp(request)
            return redirect('forgot-password-otp')  # Redirect back to OTP page after resending

        otp=request.POST['otp']
        email=request.session['email']

        otp_secret_key=request.session['otp_secret_key']
        otp_valid_until=request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until=datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp=pyotp.TOTP(otp_secret_key, interval=120)
                
                if totp.verify(otp):
                     request.session['email_']=email

                     del request.session['otp_secret_key']
                     del request.session['otp_valid_date']

                     return redirect('reset-password')
                else:
                    messages.warning(request, 'Invalid One time Password')
            else:
                messages.warning(request,'One time password has Expired')
        else:
            messages.warning(request, 'oops...something went wrong') 

    return render(request, 'user/forgot-password-otp.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        
        if password != confirm_password:
            return render(request, 'user/reset-password.html', {'error_message': 'Passwords do not match'})
        
        try:
            user = UserProfile.objects.get(email=request.session['email'])
            user.set_password(password)
            user.save()
            return redirect('password-reset-success')
        except UserProfile.DoesNotExist:
            return render(request, 'reset-password.html', {'error_message': 'Invalid email address'})

    return render(request, 'reset-password.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def password_reset_success(request):
    return render(request, 'password-reset-success.html')


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
            messages.warning(request, "Ivalid Credentials. Please try again.")      

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


@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def shop_product(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request, 'user/page-shop.html',context)




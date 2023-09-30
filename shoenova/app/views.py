from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myapp.models import Product,Category,Cart,CartItem,Variations
from .utils import send_otp,resend_otp
from datetime import datetime
import pyotp
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q


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



# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
# def login_regis(request):
#     if request.method=="POST":
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         phone=request.POST.get("phone") 
#         password=request.POST.get("password")
#         confirmpassword=request.POST.get("confirmpassword")
        
#         if password!=confirmpassword:
#             messages.warning(request, "Password is Incorrect")
#             return redirect('/login-register')
#         try:
#             if UserProfile.objects.filter(username=username).exists():
#                 messages.warning(request, "Username Is Already Taken")
#                 return redirect("/login-register")
#         except:
#             pass
#         try:
#             if UserProfile.objects.filter(email=email).exists():
#                 messages.info(request, "Email Is Already Taken")
#                 return redirect("/login-register")
#         except:
#             pass      
#         myuser = UserProfile.objects.create_user(email=email, phone=phone, password=password)
#         myuser.save()
#         messages.success(request, "Signup Successfully..Please Login!")
#         return redirect("/login-page")
#     return render(request, 'user/page-login-register.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_regis(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone") 
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        
        if password != confirmpassword:
            messages.warning(request, "Password is Incorrect")
        else:
            try:
                if UserProfile.objects.filter(username=username).exists():
                    messages.warning(request, "Username Is Already Taken")
                elif UserProfile.objects.filter(email=email).exists():
                    messages.info(request, "Email Is Already Taken")
                else:
                    myuser = UserProfile.objects.create_user(email=email, phone=phone, password=password)
                    myuser.save()
                    messages.success(request, "Signup Successfully..Please Login!")
                    return redirect("/login-page")
            except Exception as e:
                # Handle any other exceptions here
                messages.error(request, f"An error occurred: {str(e)}")

        # Retain form data after an error
        retained_data = {
            "username": username,
            "email": email,
            "phone": phone
        }
        return render(request, 'user/page-login-register.html', {'retained_data': retained_data})
    else:
        return render(request, 'user/page-login-register.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def otp_regis(request):
    if request.method=="POST":
        if 'otp_resend' in request.POST:  # Check if Resend OTP button was clicked
            resend_otp(request)
            return redirect('otp-regis')  # Redirect back to OTP page after resending

        otp=request.POST['otp']
        email=request.session['email']

        otp_secret_key=request.session.get('otp_secret_key')
        otp_valid_until=request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_until is not None:
            valid_until=datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp=pyotp.TOTP(request.session['otp_secret_key'], interval=60)

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
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            request.session['otp_secret_key'] = totp.secret 
            send_otp(request, email)
            request.session['email'] = email
            
            return redirect('otp-regis') 
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
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=products).exists()
    context={
        'products':products,
        'in_cart' :in_cart,
    }
    return render(request, 'user/shop-product-details.html',context)



@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def shop_product(request):
    products=Product.objects.all().filter(is_available=True).order_by('id')
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
    categories=Category.objects.all()
    context={
        'products':paged_products,
        'product_count':product_count,
        'categories':categories,

    }
    return render(request, 'user/page-shop.html',context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def shop_product_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    paginator=Paginator(products,9)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
    product_count = products.count()
    categories = Category.objects.all()
    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
        'selected_category': category,  # Optional: To highlight the selected category
    }
    return render(request, 'user/page-shop.html', context)



def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def add_cart(request,id):
    product=Product.objects.get(id=id)
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variations.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass    

    if product.quantity > 0:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart using cart_id present in the session
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            #existing_variations -> database
            #current_variation -> product_variation
            #item_id -> database

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()        
        return redirect('cart')
    else:
        messages.info(request, "The product is out of stock.")
        return redirect('cart')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)  
# def add_cart(request, id):
#     product = Product.objects.get(id=id)
#     product_variation = []

#     if request.method == "POST":
#         for item in request.POST:
#             key = item
#             value = request.POST[key]
            
#             try:
#                 variation = Variations.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                 product_variation.append(variation)
#             except:
#                 pass    

#     if product.quantity > 0:
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(cart_id=_cart_id(request))
#             cart.save()  # Moved this line inside the except block

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)

#             ex_var_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             # Adjusted comparison logic
#             match_found = False
#             for var_list in ex_var_list:
#                 if set(var_list) == set(product_variation):
#                     match_found = True
#                     break

#             if match_found:  # Added this condition
#                 index = ex_var_list.index(var_list)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()        
#         return redirect('cart')
#     else:
#         messages.info(request, "The product is out of stock.")
#         return redirect('cart')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def cart(request, total=0, quantity=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass 

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }     
    return render(request, 'shop-cart.html',context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def remove_cart(request,id, cart_item_id): #decrementing the the product quantity
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass        
    return redirect('cart')        




@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def delete_cart(request,id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def search(request):
    categories=Category.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-is_available').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()   
    context = {
        'products':products,
        'categories':categories,
        'product_count':product_count,
    }        
    return render(request, 'user/page-shop.html', context)

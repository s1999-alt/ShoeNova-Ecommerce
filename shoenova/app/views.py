from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myapp.models import Product, Category, Cart, CartItem, Variations, Wishlist, Banner_area
from orders.models import Order,Coupon,OrderProduct
from .utils import send_otp, resend_otp
from datetime import datetime
import pyotp
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from decimal import Decimal
from wallet.models import Wallet
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# user

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    products=Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    banner = Banner_area.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'banner': banner,
    }
    return render(request, 'user/index.html',context)


def base_view(request):
    return render(request, 'user/base.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_regis(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone") 
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        referal_id = request.POST.get("referal_id")

        if not username.strip() or not email.strip() or not phone.strip() or not password.strip() or not confirmpassword.strip():
            messages.warning(request, "Avoid the spaces and Enter the values!")
            return render(request, 'user/page-login-register.html')

        if not re.match(r'^\d+$', phone):
            messages.warning(request, "Phone number should only contain digits.")
            return render(request, 'user/page-login-register.html')

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            messages.warning(request, "Username should contain only alphanumeric characters.")
            return render(request, 'user/page-login-register.html')

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Please enter a valid email address.")
            return render(request, 'user/page-login-register.html')    
        
        
        if password != confirmpassword:
            messages.warning(request, "Password is Incorrect")
        else:
            try:
                if UserProfile.objects.filter(username=username).exists():
                    messages.warning(request, "Username Is Already Taken")
                elif UserProfile.objects.filter(email=email).exists():
                    messages.info(request, "Email Is Already Taken")
                else:
                    myuser = UserProfile.objects.create_user(email=email,
                                                             phone=phone,
                                                             password=password)
                    myuser.save()

                    if referal_id and len(referal_id) > 5:
                        try:
                            referrer = UserProfile.objects.get(referral_id=referal_id)
                            try:
                                user_wallet = Wallet.objects.get(user=referrer)
                                user_wallet.balance += 250
                                user_wallet.save()
                            except Wallet.DoesNotExist:
                                messages.error(request, 'No Wallet exists for this user.')

                            user_wallet, created = Wallet.objects.get_or_create(user=myuser, defaults={'balance': 0})
                            user_wallet.balance += 250
                            user_wallet.save()
                        except UserProfile.DoesNotExist:
                            messages.error(request, 'Invalid referral code.')
                    else:            
                        messages.success(request, "Signup Successfully..Please Login!")
                        return redirect("/login-page")
            except Exception as e:
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
            del request.session['otp_secret_key']
            del request.session['otp_valid_date']
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
                    user = get_object_or_404(UserProfile, email=email)
                    request.session['email_'] = email
                    login(request, user)

                    del request.session['email']
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('/')
                else:
                    messages.warning(request, 'Invalid One time Password')
            else:
                messages.warning(request, 'One time password has Expired')
        else:
            messages.warning(request, 'oops...something went wrong')            

    return render(request, 'user/otp.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                validate_email(email)
                totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
                request.session['otp_secret_key'] = totp.secret
                send_otp(request, email)
                request.session['email'] = email
                return redirect('forgot-password-otp')
            except ValidationError:
                messages.warning(request, "Invalid Email. Please Enter a Valid One.")
        else:
            messages.warning(request, "Please enter an email address.")
    return render(request, 'password-reset-request.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password_otp(request):
    if request.method == "POST":
        if 'otp_resend' in request.POST:
            resend_otp(request)
            return redirect('forgot-password-otp')

        otp = request.POST['otp']
        email = request.session['email']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                
                if totp.verify(otp):
                    request.session['email_']=email

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('reset-password')
                else:
                    messages.warning(request, 'Invalid One time Password')
            else:
                messages.warning(request, 'One time password has Expired')
        else:
            messages.warning(request, 'oops...something went wrong') 

    return render(request, 'user/forgot-password-otp.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if not password.strip() or not confirm_password.strip():
            messages.warning(request, "Avoid the spaces and Enter the values!")
            return render(request, 'user/reset-password.html')
        
        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
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
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart items from the user to access his product_variations    
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for i in product_variation:
                        if i in ex_var_list:
                            index = ex_var_list.index(i)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)    
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass    
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            request.session['otp_secret_key'] = totp.secret 
            send_otp(request, email)
            request.session['email'] = email
            
            return redirect('otp-regis') 
        else:
            messages.warning(request, "Ivalid Credentials. Please try again.")      

    return render(request, 'user/page-login.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def login_without_otp(request):
    
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart items from the user to access his product_variations    
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for i in product_variation:
                        if i in ex_var_list:
                            index = ex_var_list.index(i)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)    
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass    
            login(request, user)
            messages.success(request, "Login successfull !")
            return redirect('index')
        else:
            messages.warning(request, "Invalid Credentials. Please try again.")      

    return render(request, 'user/login-without-otp.html')




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
    products=Product.objects.all().filter(is_available=True)

    sort_option = request.GET.get('sort', 'featured')
    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')

    paginator=Paginator(products,3)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
    categories=Category.objects.all()

    context={
        'products':paged_products,
        'product_count':product_count,
        'categories':categories,
        'sort_option': sort_option,

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
    categories = Category.objects.all()

    sort_option = request.GET.get('sort', 'featured')

    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')

    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
        'selected_category': category,  # Optional: To highlight the selected category
        'sort_option': sort_option,
    }
    return render(request, 'user/page-shop.html', context)



def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def add_cart(request,id):
    current_user = request.user
    product=Product.objects.get(id=id)

    #if the user is authenticated
    if current_user.is_authenticated:
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


            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
            
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, user=current_user)
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
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user=current_user,
                )
                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                cart_item.save()        
            return redirect('cart')
        else:
            messages.info(request, "The product is out of stock.")
            return redirect('cart')
        
    #if the user is not authenticated    
    else:       
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




@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def cart(request, total=0, quantity=0, cart_item=None):
    cart_items = []
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price() * cart_item.quantity)
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
    product = get_object_or_404(Product, id=id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))    
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
    product = get_object_or_404(Product, id=id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))    
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def search(request):
    categories=Category.objects.all()
    products = Product.objects.none()
    product_count = 0  

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



@login_required(login_url='/login-page')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def checkout(request, total=0, quantity=0, cart_item=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price() * cart_item.quantity)
            quantity += cart_item.quantity
        
    except ObjectDoesNotExist:
        pass 
    
    coupon = None
    avlb_coupons = Coupon.objects.filter(active = True)
    coupon_discount = Decimal(0)

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj:
            coupon = coupon_obj[0]
            coupon_discount = coupon.discount
            total -= coupon.discount
            messages.success(request, 'Coupon Applied')

            request.session['coupon_code'] = coupon.coupon_code
            request.session['coupon_discount'] = float(coupon.discount)  
    
    context = {
        'total':total,
        'quantity':quantity,
        'coupon': coupon,
        'coupon_discount': float(coupon_discount),
        'cart_items':cart_items,
        'available_coupons':avlb_coupons,
    }         
    return render(request, 'checkout.html',context)


@login_required(login_url='/login-page')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def user_profile(request):
    order = Order.objects.filter(user=request.user,is_ordered=True)
    context = {
        'order': order
    }
    return render(request, 'user-profile.html', context)


@login_required(login_url='/login-page')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def order_details(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
    except Exception as e:
        print(e)
    ordered_products = OrderProduct.objects.filter(order=order)

    context = {               
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'order-details.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def wishlist_page(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to see your wishlist.')
        return redirect('/login-page/')
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist':wishlist
    }
    return render(request, 'wishlist.html', context)



@login_required(login_url='/login-page')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        existing_wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        existing_wishlist_item.save()
        messages.info(request, 'This product is already in your wishlist.')
    else:
        messages.success(request, 'Product added to your wishlist.')

    wishlist = Wishlist.objects.filter(user=request.user)  # Fetch the updated wishlist
    
    context = {
        'wishlist': wishlist
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url='/login-page')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def remove_from_wishlist(request,id):
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product__id=id)
        wishlist_item.delete()
        messages.success(request, 'Product removed from your wishlist.')
    except:
        messages.error(request, 'Product not found in your wishlist.')
    return redirect('wishlist-page')


@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def about(request):
    return render(request, 'page-about.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def contact(request):
    return render(request, 'page-contact.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def error_404(request, exception):
    return render(request,'page-404.html')







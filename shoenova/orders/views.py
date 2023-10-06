from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from myapp.models import CartItem
from .forms import OrderForm
from .models import Order,PaymentMethod,Payment,OrderProduct
from myapp.models import Variations
import datetime
import razorpay
from django.contrib import messages
from myapp.models import Product
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payments(request):
  # current_user = request.user
  # cart_items = CartItem.objects.filter(user=current_user)
  # client = razorpay.Client(auth = (settings.razor_pay_key_id , settings.key_secret))
  # payment = client.order.create({'amount' : 123465})
  # context =
  return render(request, 'user/payments.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_summary(request ,total=0, quantity=0):
  current_user = request.user

  #if the cart count is less than equal to 0, then redirect back to shop

  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()
  if cart_count <=0:
    return redirect('shop-product')
  
  for cart_item in cart_items:
    total += (cart_item.product.price * cart_item.quantity)
    quantity += cart_item.quantity

  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      # store all the billing information inside 
      data = Order()
      data.user = current_user
      data.first_name = form.cleaned_data['first_name']
      data.last_name = form.cleaned_data['last_name']
      data.phone = form.cleaned_data['phone']
      data.email = form.cleaned_data['email']
      data.address_line_1 = form.cleaned_data['address_line_1']
      data.address_line_2 = form.cleaned_data['address_line_2']
      data.country = form.cleaned_data['country']
      data.state = form.cleaned_data['state']
      data.city = form.cleaned_data['city']
      data.pin_code = form.cleaned_data['pin_code']
      data.order_note = form.cleaned_data['order_note']
      data.order_total = total
      data.ip = request.META.get('REMOTE_ADDR')
      data.save()
      #generate order number
      yr = int(datetime.date.today().strftime('%Y'))
      dt = int(datetime.date.today().strftime('%d'))
      mt = int(datetime.date.today().strftime('%m'))
      d = datetime.date(yr,mt,dt)
      current_date = d.strftime("%Y%m%d")
      order_number = current_date + str(data.id)
      data.order_number = order_number
      data.save()

      order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
      context = {
        'paymentmethods':PaymentMethod.objects.all(),
        'order':order,
        'cart_items':cart_items,
        'total':total,
      }
      return render(request, 'user/order-summary.html',context)
    
  else:
    messages.success('hellooooooo')
    return redirect('checkout')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def place_order(request, id, total=0, quantity=0):
  current_user = request.user
  #if the cart count is less than equal to 0, then redirect back to shop
  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()
  if cart_count <=0:
    return redirect('shop-product')
  
  for cart_item in cart_items:
    total += (cart_item.product.price * cart_item.quantity)
    quantity += cart_item.quantity

  if request.method == "POST":
    payment_option = request.POST['payment_option']
    order_number = request.POST['order_number']
    print(order_number)
    try:
      payment_method = PaymentMethod.objects.get(method_name=payment_option)
      order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_number)
    except Exception as e:
      print(e)

    if payment_option == 'COD':
      payment = False
    elif payment_option == 'RAZORPAY':
      payment = True

    # request.build_absolute_uri()
    success_url = request.build_absolute_uri(reverse('orders:payment-success'))    
    failed_url = request.build_absolute_uri(reverse('orders:payment-failed'))    
    context = {
      'order':order,
      'cart_items':cart_items,
      'total':total,
      'success_url':success_url,
      'failed_url':failed_url,
      'payment_method':payment_method,
      'payment':payment,
    }  
        
    return render(request, 'user/payments.html',context)
            
  order = Order.objects.get(id=id)
  context = {
    'order':order,
    'cart_items':cart_items,
    'total':total,
  }       
  return render(request, 'user/payments.html',context)
  


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment_success(request):
  method = request.GET.get('method')
  payment_id = request.GET.get('payment_id')
  payment_order_id = request.GET.get('payment_order_id')
  order_id = request.GET.get('order_id')

  if method == 'COD':
    try:
      order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_id)
     
    except Exception as e:
      print(e)
      return redirect('shop-product')
     
    payment_method_is_active =  PaymentMethod.objects.filter(method_name=method, is_active=True)
    if payment_method_is_active.exists():
      payment = Payment(
        user = request.user,
        payment_id = 'PID_COD'+ order_id,
        payment_order_id = order_id,
        payment_method = payment_method_is_active[0],
        amount_paid = order.order_total,
        status = 'SUCCESS'
      )
      payment.save()

      order.payment = payment
      order.is_ordered = True
      order.save()

      cart_items = CartItem.objects.filter(user=request.user)

      for item in cart_items:
        print(item.variations.all())
        orderproduct = OrderProduct()
        orderproduct.order = order
        orderproduct.user = request.user
        orderproduct.product = item.product
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        
        orderproduct.ordered = True
        orderproduct.save()
        orderproduct.variation.set(item.variations.all())


        product = Product.objects.get(id=item.product_id)
        product.quantity -= item.quantity
        product.save()

        CartItem.objects.filter(user=request.user).delete()

        request.session["order_number"] = order_id
        request.session["payment_id"] = 'PID-COD'+order_id
        return redirect('orders:payment-success-page')
      
      else:
        messages.error(request, "Invalid Payment Method Found")
        return redirect('payment-failed')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment_failed(request):
  return HttpResponse('failed')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment_success_page(request):
  return render(request, 'user/payment-success-page.html')


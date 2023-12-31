from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from myapp.models import CartItem
from .forms import OrderForm
from .models import Order,PaymentMethod,Payment,OrderProduct,Coupon, Invoice
from myapp.models import Variations
from wallet.models import Wallet,WalletTransaction
import datetime
import razorpay
from django.contrib import messages
from myapp.models import Product
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from django.http import JsonResponse
import json
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import get_template
import datetime



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payments(request):
  return render(request, 'user/payments.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_summary(request ,total=0, quantity=0):
  current_user = request.user
  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()

  #if the cart count is less than equal to 0, then redirect back to shop
  if cart_count <=0:
    return redirect('shop-product')
  
  for cart_item in cart_items:
    total += (cart_item.product.product_price() * cart_item.quantity)
    quantity += cart_item.quantity
  

  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      # store all the billing information inside 
      coupon_discount = 0
      coupon_code = request.POST.get('coupon','')
      print(coupon_code)
      coupon = None
      if coupon_code:
          try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            coupon_discount = coupon.discount
            total -= coupon_discount
          except Exception as e:
            
            print(e)
            
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
      data.coupon = coupon
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
     

      wallet = Wallet.objects.get_or_create(user=request.user, is_active=True)

      context = {
        'paymentmethods':PaymentMethod.objects.all(),
        'order':order,
        'cart_items':cart_items,
        'total':total,
        'wallet':wallet,
        'coupon_discount':coupon_discount,
      }
      return render(request, 'user/order-summary.html',context)
    context = {
      'paymentmethods': PaymentMethod.objects.all(),
      'order': order,
      'cart_items': cart_items,
      'total': total,
      'wallet':wallet,
      'coupon_discount':coupon_discount,
    }
    return render(request, 'user/order-summary.html', context)
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
    total += (cart_item.product.product_price() * cart_item.quantity)
    quantity += cart_item.quantity

  if request.method == "POST":
    if request.POST.get('wallet_balance'):
      wallet_selected = int(request.POST.get('wallet_balance'))
    else:
      wallet_selected = request.POST.get('wallet_balance')

    order_number = request.POST['order_number']
    payment_option = request.POST['payment_option']
    

    if not payment_option:
      messages.error(request, "please choose a payment method")
      return redirect('order_summary')

    try:
      payment_method = PaymentMethod.objects.get(method_name=payment_option)
      order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_number)
      if order.coupon:
        total -= order.coupon.discount
        coupon_discount = order.coupon.discount    
    except Exception as e:
      print(e)
    
    if wallet_selected == 1:
      wallet = Wallet.objects.get(user=request.user, is_active=True)
      if wallet.balance <= total:
        total -= wallet.balance
        order.wallet_discount = wallet.balance
        order.order_total = total
      else:
        order.wallet_discount = total
        order.order_total = 0
    else:
      order.order_total = total
      order.wallet_discount=0
    order.save()

    try:
      if total == 0:
        raise Exception  
      if payment_option == 'COD':
        payment = False
      elif payment_option == 'RAZORPAY':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount':float(total)*100, "currency":"INR"})
      else:
        payment = False
    except:
      payment = False
    
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
      'coupon_discount':coupon_discount,
    }  
    print(payment)    
    return render(request, 'user/payments.html',context)         
  order = Order.objects.get(id=id)
  context = {
    'order':order,
    'cart_items':cart_items,
    'total':total,
    'coupon_discount':coupon_discount,
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

      wallet = Wallet.objects.get(user=request.user, is_active=True)
      wallet.balance = wallet.balance - order.wallet_discount
      wallet.save()

      wallet_transaction = WalletTransaction.objects.create(
        wallet = wallet,
        transaction_type = 'DEBIT',
        order = order,
        transaction_detail = str(order.order_number),
        amount = order.wallet_discount
      )
      wallet_transaction.save()

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
        orderproduct.product_price = item.product.product_price()
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

  elif method == 'RAZORPAY':
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_id)
    payment_method_is_active = PaymentMethod.objects.filter(method_name = method, is_active = True)

    if payment_method_is_active.exists():
      payment = Payment(
        user = request.user,
        payment_id = payment_id,
        payment_order_id = payment_order_id,
        payment_method = payment_method_is_active[0],
        amount_paid = order.order_total,
        status = 'SUCCESS',
      )
      payment.save()

      wallet = Wallet.objects.get(user=request.user, is_active = True)
      wallet.balance = wallet.balance - order.wallet_discount
      wallet.save()

      wallet_transaction = WalletTransaction.objects.create(
        wallet = wallet,
        transaction_type = 'DEBIT',
        order = order,
        transaction_detail = str(order.order_number),
        amount = order.wallet_discount
      )
      wallet_transaction.save()

      order.payment = payment
      order.is_ordered = True
      order.save()

      cart_items = CartItem.objects.filter(user = request.user)

      for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order= order
        orderproduct.user = request.user
        orderproduct.product = item.product
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.product_price()

        orderproduct.ordered = True
        orderproduct.save()
        orderproduct.variation.set(item.variations.all())

        product = Product.objects.get(id=item.product_id)
        product.quantity -= item.quantity
        product.save()

      CartItem.objects.filter(user=request.user).delete()

      request.session["order_number"] = order_id
      request.session["payment_id"] = payment_id
      return redirect('orders:payment-success-page')
      
    else:
      messages.error(request, "Invalid Payment Method Found")
      return redirect('payment-failed')
    
  elif method == 'WALLET':
    payment_method_is_active = PaymentMethod.objects.filter(method_name = method, is_active = True)
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_id)

    payment = Payment(
      user = request.user,
      payment_order_id = order_id,
      payment_method = payment_method_is_active[0],
      amount_paid = order.order_total,
      payment_id = 'PID-WLT' + order_id,
      status = 'SUCCESS',
    )
    payment.save()

    wallet = Wallet.objects.get(user=request.user, is_active=True)
    wallet.balance = wallet.balance - order.wallet_discount
    wallet.save()

    wallet_transaction = WalletTransaction.objects.create(
      wallet = wallet,
      transaction_type = 'DEBIT',
      order = order,
      transaction_detail = str(order.order_number),
      amount = order.wallet_discount
      )
    wallet_transaction.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user = request.user)

    for item in cart_items:
      orderproduct = OrderProduct()
      orderproduct.order= order
      orderproduct.user = request.user
      orderproduct.product = item.product
      orderproduct.quantity = item.quantity
      orderproduct.product_price = item.product.product_price()

      orderproduct.ordered = True
      orderproduct.save()
      orderproduct.variation.set(item.variations.all())

      product = Product.objects.get(id=item.product_id)
      product.quantity -= item.quantity
      product.save()

      CartItem.objects.filter(user=request.user).delete()

      request.session["order_number"] = order_id
      request.session["payment_id"] = 'PID-WLT' + payment_id
      return redirect('orders:payment-success-page')
    
  else:
    return redirect('user-profile')   
        



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment_failed(request):
  return HttpResponse('failed')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment_success_page(request):

  order_id = request.session["order_number"]

  order = Order.objects.get(user = request.user,order_number = order_id)
  invoice = Invoice()
  invoice.order = order
  invoice.save()

  return render(request, 'user/payment-success-page.html',context={'invoice':invoice,'order':order})



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_cancel_user(request,order_number):
  order = Order.objects.get(order_number=order_number)
  if not order.status == 'Cancelled':
    order.status = 'Cancelled'
    order.save()
    wallet = Wallet.objects.get(user=request.user, is_active=True)
    wallet.balance += float(order.order_total + order.wallet_discount)
    wallet.save()

    wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                          transaction_type='CREDIT',
                                                          transaction_detail=str(order.order_number)+ 'CANCELLED',
                                                          amount = order.wallet_discount)
    wallet_transaction.save()
    return redirect('order-details', order_number=order.order_number)
  else:
    return redirect('order-details', order_number=order.order_number)
  


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_return_user(request,order_number):
  order = Order.objects.get(order_number=order_number)
  if not order.status == 'Returned':
    order.status = 'Returned'
    order.save()
    wallet = Wallet.objects.get(user=request.user, is_active=True)
    wallet.balance += float(order.order_total + order.wallet_discount)
    wallet.save()

    wallet_transaction = WalletTransaction.objects.create(wallet=wallet,
                                                          transaction_type='CREDIT',
                                                          transaction_detail=str(order.order_number)+ 'Returned',
                                                          amount = order.wallet_discount)
    wallet_transaction.save()
    return redirect('order-details', order_number=order.order_number)
  else:
    return redirect('order-details', order_number=order.order_number)  
  
  

def get_weekly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(weekly_sales=Sum('quantity'))



def get_monthly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(monthly_sales=Sum('quantity'))



def get_yearly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=365)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(yearly_sales=Sum('quantity'))



def sales_report(request):
    weekly_sales_data = list(get_weekly_sales().values('product__product_name','weekly_sales'))  # Convert QuerySet to a list of dictionaries
    monthly_sales_data = list(get_monthly_sales().values('product__product_name','monthly_sales'))
    yearly_sales_data = list(get_yearly_sales().values('product__product_name','yearly_sales'))
    sales_data = {
        'weekly_sales': weekly_sales_data,
        'monthly_sales': monthly_sales_data,
        'yearly_sales': yearly_sales_data,
    }
    return JsonResponse(sales_data, safe=False)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def generate_invoice(request, invoice_number):
  try:
    invoice = Invoice.objects.get(invoice_number = invoice_number)
  except:
    messages.warning(request, 'Invoice not generated for this order!')

  try:
    order_products = OrderProduct.objects.filter(order = invoice.order)

  except Exception as  e:
    print(e)

  sub_total = 0

  for i in order_products:
    sub_total += i.product_price * i.quantity

  template_path = 'user/invoice_pdf.html'
  context = {
    'invoice' : invoice,
    'ordered_products' : order_products,
    'sub_total' : sub_total,
    'payable_amount' : invoice.order.order_total,
    'order' : invoice.order,
  }

  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'filename="{invoice.invoice_number}"'
  template = get_template(template_path)
  html = template.render(context)


  pisa_status = pisa.CreatePDF(
    html, dest=response)

  if pisa_status.err:
    return HttpResponse('We had some errors <pre>' + html + '</pre>')
  return response              








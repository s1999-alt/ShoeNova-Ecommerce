from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime


def place_order(request, total=0, quantity=0):
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
      return redirect('checkout')
    
  else:
    return redirect('checkout')





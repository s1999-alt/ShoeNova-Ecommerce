from django.shortcuts import render
from wallet.models import Wallet
import json
from orders.models import Order
from django.http import JsonResponse


# Create your views here.
 
def wallet(request):
  wallet,created = Wallet.objects.get_or_create(user=request.user, is_active=True)
  context = {
    'wallet': wallet
  }
  return render(request, 'user/wallet.html', context)



def get_wallet_grand_total(request):
    order_number = request.GET.get('order_number')
    check = request.GET.get('check')
    if order_number:
        
        wallet = Wallet.objects.get(user=request.user,is_active=True)
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        grand_total = order.order_total
        wallet_balance = wallet.balance  
        
        if check=='true':  
            if wallet.balance <= grand_total  :  
                grand_total = grand_total- wallet.balance   
                wallet_balance = 0
            else:
                wallet_balance = wallet.balance - grand_total
                grand_total = 0
                    
            return JsonResponse({"status": "success", "grand_total":grand_total,"wallet_balance":wallet_balance})
        else:
            return JsonResponse({"status": "success", "grand_total":grand_total,"wallet_balance":wallet_balance})

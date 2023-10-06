from myapp.models import Cart,CartItem,Wishlist
from .views import _cart_id




def counter(request):
  if 'admin' in request:
    return {}
  
  else:
    cart_count = 0
    try:
      cart = Cart.objects.filter(cart_id=_cart_id(request))
      if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user=request.user)
      else:  
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
      for cart_item in cart_items:
        cart_count += cart_item.quantity
    except Cart.DoesNotExist:
      cart_count = 0
  return dict(cart_count=cart_count)



def wishlist_counter(request):
  if 'admin' in request:
    return {}
  
  else:
    wishlist_count = 0
    try:
      if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_count = len(wishlist_items)
    except:
      wishlist_count = 0
  return dict(wishlist_count = wishlist_count)    


  



from django.shortcuts import render,redirect, HttpResponse
from myapp.models import Product,Category, Wishlist
from .models import CategoryOffer,ProductOffer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def offers(request):
  category_offer = CategoryOffer.objects.all()
  context = {
    'category_offer':category_offer
  }
  return render(request, 'offers.html', context)



def category_offer_product(request, offer_slug, category=None):

  try:
    category_offer = get_object_or_404(CategoryOffer, category_offer_slug=offer_slug)
  except:
    return redirect('shop-product')

  category = category_offer.category

  if category:
    # category = category_offer.category.filter(is_available=True, slug = category)
    products = Product.objects.filter(category=category)
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
    categories=[category]
    context={
          'products':paged_products,
          'product_count':product_count,
          'categories':categories,

      }
    return render(request, 'user/page-shop.html',context)
  else:
      products = Product.objects.filter(category=category)
      paginator=Paginator(products,3)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)
      product_count=products.count()
      categories=[category]

      context={
            'products':paged_products,
            'product_count':product_count,
            'categories':categories,

        }
      return render(request, 'user/page-shop.html',context)



















def add_category_offer(request):
  if request.method == "POST":
    offer_name = request.POST['offer_name']
    expire_date = request.POST['expire_date']
    category_id = request.POST['category']
    category = Category.objects.get(id=category_id)
    dis_percentage = request.POST['dis_percentage']
    cat_offer_image = request.FILES.get('cat_offer_image')
    is_active = request.POST['is_active']

    if is_active == 'on':
      is_active = True
    else:
      is_active = False  

    try:
      category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
      return HttpResponse("Category does not exist.")

    categoryoffer = CategoryOffer(
      offer_name = offer_name,
      expire_date = expire_date,
      category = category,
      discount_percentage = dis_percentage,
      category_offer_image = cat_offer_image,
      is_active = is_active,
    )
    categoryoffer.save()
    return redirect('offers:add-category-offer') 

  categories = Category.objects.all()
  context = {
    'categories': categories 
  }
  return render(request, 'admin-side/add-category-offers.html',context)
















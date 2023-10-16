from django.shortcuts import render
from myapp.models import Product,Category


def add_category_offer(request):
  categories = Category.objects.all()
  context = {
    'categories': categories 
  }
  return render(request, 'admin-side/add-category-offers.html',context)

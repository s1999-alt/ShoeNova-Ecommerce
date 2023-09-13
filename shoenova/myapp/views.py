from django.shortcuts import render,redirect
from myapp.models import Product,Category
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.


#admin
def adm_index(request):
    return render(request, 'admin-side/index.html')



#-----------Product list-view page------------------
def admn_product_list(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'admin-side/page-products-list.html',context)



#-------------Add Product------------------
def admn_add_product(request):
    if request.method=="POST":
        product_name=request.POST.get("product_name")
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        brand=request.POST.get("brand")
        description=request.POST.get("description")
        price=request.POST.get("price")
        quantity=request.POST.get("quantity")
        product_images=request.FILES.get('product_images')
        slug = slugify(product_name)
        count = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1

        product=Product(
            product_name=product_name,
            category=category,
            brand=brand,
            description=description,
            price=price,
            quantity=quantity,
            product_images=product_images,
            slug=slug
        )    
        product.save()
        return redirect('admn-product-list')
    
    categories=Category.objects.all()
    context={
        'categories':categories
    }

    return render(request, 'admin-side/page-add-product.html',context)



def admn_product_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'admin-side/page-categories.html',context)






def admn_add_categories_page(request):
     return render(request, 'admin-side/page-add-categories.html')

#-------------Add categories------------------
def admn_add_categories(request):
    if request.method=="POST":
        category_name=request.POST.get("category_name")
        slug=request.POST.get("slug")
        description=request.POST.get("description")

       
        categories=Category(
            category_name=category_name,
            slug=slug,
            description=description
        )
        categories.save()
        return redirect('myapp:admn_product_category')
    
    messages.warning(request,'Unexpected error occurred, please retry.')
    return render(request, 'admin-side/page-add-categories.html')



def admn_users_list(request):
    return render(request, 'admin-side/page-users-list.html')

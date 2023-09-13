from django.shortcuts import render,redirect,HttpResponse
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

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return HttpResponse("Category does not exist.")    

        product=Product(
            product_name=product_name,
            category=category,
            brand=brand,
            description=description,
            price=price,
            quantity=quantity,
            slug=slug,
            product_images=product_images,
        )    
        
        product.save() 
        return redirect('myapp:admn-product-list')
    
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    messages.success(request,'Product Added Succcessfully..')
    return render(request, 'admin-side/page-add-product.html',context)


#--------------category list view page-----------------
def admn_product_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'admin-side/page-categories.html',context)




#-------------Add categories------------------
def admn_add_categories(request):
    if request.method=="POST":
        category_name=request.POST.get("category_name")
        slug=request.POST.get("slug")
        description=request.POST.get("description")

        if not category_name or not slug or not description:
            messages.warning(request,"please fill in all required fields")
            return render(request, 'admin-side/page-add-categories.html')

       
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

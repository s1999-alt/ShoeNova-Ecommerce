from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myapp.models import Product,Category
from django.utils.text import slugify
from django.contrib import messages
from app.models import UserProfile

# Create your views here.

#----------admin index page------------------------

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def adm_index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        messages.success(request, 'Login Successfully')
        return render(request, 'admin-side/index.html')
    return render(request, 'admin-side/page-admin-login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_login(request):
        if request.user.is_authenticated and request.user.is_superuser:
            messages.success(request, 'Login Successfully')
            return render(request, 'admin-side/index.html')
        
        if request.method=='POST':
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
       

            if user is not None and user.is_superuser:
                login(request,user)
                request.session['email']=user.email
                messages.success(request, "Login Successfully")
                return redirect('myapp:admin-index')
            else:
                 messages.error(request,'Invalid credentials or not a superuser.')

        return render(request, 'admin-side/page-admin-login.html')

@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    if 'email' in request.session:
        del request.session['email']
    logout(request)
    messages.info(request,"Logout Successfully")
    return render(request, 'admin-side/page-admin-login.html')    




    





########################## ADMIN-PRODUCT ################################

#-----------Product list-view page------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_product_list(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'admin-side/page-products-list.html',context)

#-------------Add Product---------------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_add_product(request):
    if request.method=="POST":
        product_name=request.POST.get("product_name")
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        brand=request.POST.get("brand")
        description=request.POST.get("description")
        price=request.POST.get("price")
        max_price=request.POST.get("max_price")
        quantity=request.POST.get("quantity")
        product_images=request.FILES.get('product_images')
        product_images2=request.FILES.get('product_images2')
        product_images3=request.FILES.get('product_images3')
        product_images4=request.FILES.get('product_images4')
        product_images5=request.FILES.get('product_images5')
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
            max_price=max_price,
            quantity=quantity,
            slug=slug,
            product_images=product_images,
            product_images2=product_images2,
            product_images3=product_images3,
            product_images4=product_images4,
            product_images5=product_images5,
        )    

        product.save() 
        return redirect('myapp:admn-product-list')
    
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    messages.success(request,'Product Added Succcessfully..')
    return render(request, 'admin-side/page-add-product.html',context)

#--------------Delete product--------------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    if product.soft_deleted:
        product.soft_deleted=False
    else:
        product.soft_deleted=True
    product.save()    
    return redirect('myapp:admn-product-list')

#-----------------Edit Product---------------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_edit_product(request,id):
    product=Product.objects.get(id=id)
    categories=Category.objects.all()

    if request.method=='POST':
        product.product_name=request.POST.get('product_name')
        category_id=request.POST.get('category')
        product.category = Category.objects.get(id=category_id) 
        product.brand=request.POST.get('brand')
        product.description=request.POST.get('description')
        product.price=request.POST.get('price')
        product.quantity=request.POST.get('quantity')
        product.product_images=request.FILES.get('product_images')
        product.product_images2=request.FILES.get('product_images2')
        product.product_images3=request.FILES.get('product_images3')
        product.product_images4=request.FILES.get('product_images4')
        product.product_images5=request.FILES.get('product_images5')
        product.save()
        return redirect('myapp:admn-product-list')
    return render(request, 'admin-side/page-edit-products.html', {'product': product,'categories': categories})




######################### ADMIN-CATEGORY #####################################

#--------------category list view page-----------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_product_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'admin-side/page-categories.html',context)

#-------------Add categories------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_add_categories(request):
    if request.method=="POST":
        category_name=request.POST.get("category_name")
        slug=request.POST.get("slug")
        description=request.POST.get("description")
        category_images=request.FILES.get("category_images")


        if not category_name or not slug or not description or not category_images:
            messages.warning(request,"please fill in all required fields")
            return render(request, 'admin-side/page-add-categories.html')
       
        categories=Category(
            category_name=category_name,
            slug=slug,
            description=description,
            category_image=category_images,


        )
        categories.save()
        messages.success(request, 'Category Added Successfully')
        return redirect('myapp:admn_product_category')
    return render(request, 'admin-side/page-add-categories.html')

#----------------category Enable-Disable-------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_enable_disable_categories(request,id):
    category=Category.objects.get(id=id)
    try:
        if category.soft_deleted:
            category.soft_deleted=False
            category.save()
            messages.success(request,'Category Enabled')
            return redirect('admn_product_category')
        else:
            category.soft_deleted=True
            category.save()
            messages.warning(request,'Category Disabled')
    except:
        messages.warning(request,'Error Occured')
    return redirect('myapp:admn_product_category')

#--------------------Edit categories---------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_edit_categories(request,id):
    category=Category.objects.get(id=id)

    if request.method=='POST':
        category.category_name=request.POST.get('category_name')
        category.slug=request.POST.get('slug')
        category.description=request.POST.get('description')
        category.category_image=request.FILES.get('category_images')
        category.save()
        return redirect('myapp:admn_product_category')
    context={
        'category':category
    }
    return render(request, 'admin-side/page-edit-categories.html',context)

#-------------------Category delete----------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_delete_categories(request,id):
    category= get_object_or_404(Category,id=id)
    category.delete()
    return redirect('myapp:admn_product_category')





#--------------------Admin side user list page------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_users_list(request):
    users=UserProfile.objects.all().exclude(is_superuser=True)
    context={
        'users':users
    }
    return render(request, 'admin-side/page-users-list.html',context)

#------------------Admin side user block unblock-------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_users_block_unblock(request,id):
    user=UserProfile.objects.get(id=id)
    try:
        if user.is_blocked:
            user.is_blocked=False
            user.is_active=True
            user.save()
            messages.success(request, 'User is Unblocked')
        else:
            user.is_blocked=True
            user.is_active=False
            user.save()
            messages.warning(request, 'User is Blocked')
    except UserProfile.DoesNotExist:
        messages.warning(request,'User does not Exist')
    return redirect('myapp:admn_users_list')    









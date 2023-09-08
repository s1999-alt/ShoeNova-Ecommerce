from django.shortcuts import render

# Create your views here.


#admin
def adm_index(request):
    return render(request, 'admin-side/index.html')

def admn_product_list(request):
    return render(request, 'admin-side/page-products-list.html')

def admn_product_category(request):
    return render(request, 'admin-side/page-categories.html')

def admn_users_list(request):
    return render(request, 'admin-side/page-users-list.html')

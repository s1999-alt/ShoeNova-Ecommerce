from django.shortcuts import render

# Create your views here.


#admin
def adm_index(request):
    return render(request, 'admin-side/index.html')

def Admn_product_list(request):
    return render(request, 'admin-side/page-products-list.html')

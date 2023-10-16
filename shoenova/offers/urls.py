from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
  path('add-category-offer', views.add_category_offer, name='add-category-offer'),


]

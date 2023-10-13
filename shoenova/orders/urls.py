from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
  path('place_order/', views.place_order, name='place_order'),
  path('payments/', views.payments, name='payments'),
  path('order_summary/', views.order_summary, name='order_summary'),
  path('place_order/<int:id>', views.place_order, name='place_order'),
  path('payment/payment-success', views.payment_success, name='payment-success'),
  path('payment/payment-failed/', views.payment_failed, name='payment-failed'),
  path('payment-success-page/', views.payment_success_page, name='payment-success-page'),


  path('order-cancel-user/<int:order_number>', views.order_cancel_user, name='order-cancel-user'),

  path('sales-report', views.sales_report, name='sales-report'),

  path('generate-invoice/<str:invoice_number>', views.generate_invoice, name='generate-invoice'),

]


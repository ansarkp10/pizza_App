# home/urls.py
from django.urls import path
from .views import home, order_pizza, order
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('api/order', order_pizza, name='order_pizza'),
    path('<order_id>/', order, name='order'),
    path('print-invoice/<str:order_id>/', views.print_invoice, name='print_invoice'),
]

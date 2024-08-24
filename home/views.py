from django.shortcuts import render, redirect
from .models import Pizza, Order
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    pizza = Pizza.objects.all()
    
    # Check if the user is authenticated before filtering orders
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.none()  # Return an empty queryset if the user is not authenticated
    
    context = {'pizza': pizza, 'orders': orders}
    return render(request, 'index.html', context)

def order(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('/')
    
    context = {'order': order}
    return render(request, 'order.html', context)

@csrf_exempt
def order_pizza(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    data = json.loads(request.body)
    
    try:
        pizza = Pizza.objects.get(id=data.get('id'))
        order = Order(user=user, pizza=pizza, amount=pizza.price)
        order.save()

        # Prepare the order data to be sent back to the frontend
        order_data = {
            'order_id': order.order_id,
            'date': order.date.strftime('%Y-%m-%d %H:%M'),
            'status': order.status,
            'amount': order.amount,
        }

        return JsonResponse({'message': 'Success', 'order': order_data})

    except Pizza.DoesNotExist:
        return JsonResponse({'error': 'Pizza does not exist'})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order  # Adjust the import based on your project structure
from xhtml2pdf import pisa

from .models import Order

def print_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = order.items.all()  # Fetch all related OrderItem instances
    
    # Prepare data for each item in the order
    items_data = []
    for item in order_items:
        items_data.append({
            'pizza_name': item.pizza.name,
            'quantity': item.quantity,
            'unit_price': item.pizza.price,
            'total_price': item.total_price
        })
    
    total_amount = sum(item['total_price'] for item in items_data)
    
    context = {
        'order': order,
        'order_items_data': items_data,  # Pass the items data to the template
        'total_amount': total_amount,
    }
    return render(request, 'invoice_template.html', context)

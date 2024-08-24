from django.db import models
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer

# Create your models here.

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    image = models.ImageField(upload_to='pizzas/')

    def __str__(self):
        return self.name

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = (
    ("Order Received", "Order Received"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Delivered", "Delivered"),
)

class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default=1)  # Replace 1 with a valid pizza ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField(default=100)  # Unit price
    status = models.CharField(max_length=100, choices=CHOICES, default="Order Received")
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.amount * self.quantity  # Total amount calculation

    def save(self, *args, **kwargs):  
        if not self.order_id:
            self.order_id = random_string_generator()
        self.amount = self.pizza.price  # Ensure the unit price matches the pizza price
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.pizza.name}"

    @staticmethod
    def give_order_details(order_id):
        instance = Order.objects.filter(order_id=order_id).first()
        data = {
            'order_id': instance.order_id,
            'amount': instance.amount,
            'status': instance.status,
            'date': str(instance.date),
        }
        return data

@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            'order_id': instance.order_id,
            'amount': instance.amount,
            'status': instance.status,
            'date': str(instance.date),
        }
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)

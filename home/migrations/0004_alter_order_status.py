# Generated by Django 5.1 on 2024-08-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Recieved', 'Order Recieved'), ('Baking', 'Baking'), ('Baked', 'Baked'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Order Recieved', max_length=100),
        ),
    ]

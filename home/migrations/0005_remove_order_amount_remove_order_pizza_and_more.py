# Generated by Django 5.1 on 2024-08-23 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='pizza',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Received', 'Order Received'), ('Baking', 'Baking'), ('Baked', 'Baked'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Order Received', max_length=100),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='home.order')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pizza')),
            ],
        ),
    ]

# Generated by Django 5.1 on 2024-08-23 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(upload_to='pizzas/'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-08-01 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_cartitem_name_remove_cartitem_price_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('user', 'product')},
        ),
    ]

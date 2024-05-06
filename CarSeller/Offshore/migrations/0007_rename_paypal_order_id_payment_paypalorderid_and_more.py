# Generated by Django 4.2 on 2024-05-05 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Offshore', '0006_rename_stripe_order_id_payment_paypal_order_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='paypal_order_id',
            new_name='paypalOrderId',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='paypal_payment_id',
            new_name='paypalPaymentID',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='paypal_payment_status',
            new_name='paypalPaymentStatus',
        ),
    ]
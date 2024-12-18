# Generated by Django 4.2 on 2024-04-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offshore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('features', models.TextField()),
                ('brand', models.CharField(choices=[('FD', 'Ford'), ('MD', 'Mercedez'), ('FR', 'Ferrari'), ('LB', 'Lamborghini'), ('MB', 'Maybach'), ('BG', 'Buggati')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]

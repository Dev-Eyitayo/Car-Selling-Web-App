# Generated by Django 4.2 on 2024-04-19 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('brand', models.CharField(choices=[('FD', 'Ford'), ('MD', 'Mercedez'), ('FR', 'Ferrari'), ('LB', 'Lamborghini'), ('MB', 'Maybach'), ('BG', 'Buggati')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
# Generated by Django 3.2.1 on 2021-06-20 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0012_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myshop.product')),
            ],
        ),
    ]
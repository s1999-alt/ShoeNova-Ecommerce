# Generated by Django 4.2.4 on 2023-09-13 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_offer_price_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(upload_to='photos/categories'),
        ),
    ]
# Generated by Django 4.2.4 on 2023-10-16 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_producct_wishlist_product'),
        ('offers', '0002_rename_product_offer_images_categoryoffer_category_offer_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryoffer',
            name='category',
        ),
        migrations.AddField(
            model_name='categoryoffer',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.category'),
            preserve_default=False,
        ),
    ]

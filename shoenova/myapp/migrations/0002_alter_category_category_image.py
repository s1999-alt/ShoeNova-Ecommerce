# Generated by Django 4.2.4 on 2023-09-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(blank=True, upload_to='photos/categories'),
        ),
    ]

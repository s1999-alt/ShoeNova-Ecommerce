# Generated by Django 4.2.4 on 2023-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_variations'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='myapp.variations'),
        ),
    ]

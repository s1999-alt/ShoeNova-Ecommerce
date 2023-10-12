# Generated by Django 4.2.4 on 2023-10-12 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_order_wallet_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.order')),
            ],
        ),
    ]

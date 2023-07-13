# Generated by Django 4.2 on 2023-07-13 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'корзина',
                'verbose_name_plural': 'корзины',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='количество')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='cart.cart', verbose_name='товары')),
            ],
            options={
                'verbose_name': 'позиция в корзине',
                'verbose_name_plural': 'позиции в корзине',
                'ordering': ('-date_added',),
            },
        ),
    ]

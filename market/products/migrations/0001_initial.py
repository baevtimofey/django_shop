# Generated by Django 4.2 on 2023-06-30 15:37

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import products.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=512, verbose_name='наименование')),
                ('description', models.CharField(max_length=512, verbose_name='описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='./static/img/icons/departments/', verbose_name='иконка')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='products.category', verbose_name='родительская категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=512, verbose_name='наименование')),
                ('description', models.TextField(blank=True, max_length=2048, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлён')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='наименование')),
            ],
            options={
                'verbose_name': 'свойство',
                'verbose_name_plural': 'свойства',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', taggit.managers.TaggableManager(help_text='Список тегов, разделенных запятыми.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=128, verbose_name='значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_properties', to='products.product', verbose_name='продукт')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_properties', to='products.property', verbose_name='свойство')),
            ],
            options={
                'verbose_name': 'свойство продукта',
                'verbose_name_plural': 'свойства продукта',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.upload_product_image, verbose_name='изображение')),
                ('description', models.TextField(blank=True, max_length=2048, verbose_name='описание')),
                ('ord_number', models.PositiveSmallIntegerField(blank=True, null=True, unique=True, verbose_name='порядковый номер')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'ordering': ['ord_number'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='property',
            field=models.ManyToManyField(related_name='products', through='products.ProductProperty', to='products.property', verbose_name='характеристики'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.producttag', verbose_name='теги'),
        ),
    ]
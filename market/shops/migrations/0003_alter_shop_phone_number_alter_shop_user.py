# Generated by Django 4.2 on 2023-07-11 08:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='phone_number',
            field=models.CharField(blank=True, max_length=18, null=True, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть введен в формате: '+7 (123) 456-78-90'. Максимальная длина 12 символов.", regex='^\\+\\d{1,3}\\s\\(\\d{3}\\)\\s\\d{3}-\\d{2}-\\d{2}$')], verbose_name='номер телефона'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

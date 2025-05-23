# Generated by Django 4.2.10 on 2025-05-14 07:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+628..'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('total_lontong_large', models.PositiveIntegerField(default=0)),
                ('total_lontong_small', models.PositiveIntegerField(default=0)),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

# Generated by Django 4.2.17 on 2025-01-05 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0009_ad_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]

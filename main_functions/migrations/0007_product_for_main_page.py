# Generated by Django 3.0.8 on 2021-06-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_functions', '0006_auto_20210605_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='for_main_page',
            field=models.BooleanField(default=False),
        ),
    ]
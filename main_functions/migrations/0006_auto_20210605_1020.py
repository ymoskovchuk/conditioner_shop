# Generated by Django 3.0.8 on 2021-06-05 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_functions', '0005_auto_20210603_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('AUX', 'AUX'), ('Cooper&Hunter', 'Cooper&Hunter'), ('Daikin', 'Daikin'), ('Gree', 'Gree'), ('Hitachi', 'Hitachi'), ('Leberg', 'Leberg'), ('LG', 'LG'), ('Mitsubishi Electric', 'Mitsubishi Electric'), ('Mitsubishi Heavy', 'Mitsubishi Heavy'), ('Neoclima', 'Neoclima'), ('Olmo', 'Olmo'), ('Panasonic', 'Panasonic'), ('Samsung', 'Samsung'), ('Smartway', 'Smartway'), ('Toshiba', 'Toshiba')], max_length=255, verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='product',
            name='invertor_power',
            field=models.CharField(blank=True, choices=[('7 BTU', '7 BTU'), ('9 BTU', '9 BTU'), ('12 BTU', '12 BTU'), ('18 BTU', '18 BTU'), ('24 BTU', '24 BTU')], max_length=255, null=True, verbose_name='Потужність інвертора'),
        ),
    ]

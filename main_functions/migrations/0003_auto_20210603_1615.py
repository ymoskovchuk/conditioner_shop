# Generated by Django 3.0.8 on 2021-06-03 13:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_functions', '0002_auto_20210602_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='conditioner_type',
            field=models.CharField(choices=[('Настінні спліт-системи', 'Настінні спліт-системи'), ('Мультиспліт-системи', 'Мультиспліт-системи'), ('Мобільні кондиціонери', 'Мобільні кондиціонери'), ('Кондиціонери на стелю', 'Кондиціонери на стелю'), ('Касетні кондиціонери', 'Касетні кондиціонери'), ('Канальні кондиціонери', 'Канальні кондиціонери')], default=django.utils.timezone.now, max_length=255, verbose_name='Тип кондиціонера'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='invertor_power',
            field=models.CharField(blank=True, choices=[('7 BTU', '7 BTU'), ('9 BTU', '9 BTU'), ('12 BTU', '12 BTU'), ('18 BTU', '18 BTU'), ('24 BTU', '24 BTU'), ('24 BTU', '24 BTU')], max_length=255, null=True, verbose_name='Потужність інвертора'),
        ),
        migrations.AlterField(
            model_name='product',
            name='air_consumption',
            field=models.CharField(max_length=255, verbose_name='Споживання повітря, м³/год. '),
        ),
        migrations.AlterField(
            model_name='product',
            name='invertor',
            field=models.CharField(choices=[('Так', 'Так'), ('Ні', 'Ні')], max_length=255, verbose_name='Інвертор'),
        ),
    ]
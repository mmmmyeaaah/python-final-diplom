# Generated by Django 4.1.5 on 2023-02-01 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакты пользователя', 'verbose_name_plural': 'Контакты пользователей'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-dt'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['-name'], 'verbose_name': 'Магазин', 'verbose_name_plural': 'Магазины'},
        ),
    ]

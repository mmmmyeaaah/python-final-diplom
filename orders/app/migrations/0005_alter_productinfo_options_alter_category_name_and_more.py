# Generated by Django 4.1.5 on 2023-01-24 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_shop_filename'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinfo',
            options={'ordering': ['-name'], 'verbose_name': 'Информация о продукте', 'verbose_name_plural': 'Информация о продуктах, остатки'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название продукта'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_info', to='app.shop', verbose_name='Магазин'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название магазина'),
        ),
        migrations.AddConstraint(
            model_name='productinfo',
            constraint=models.UniqueConstraint(fields=('product', 'shop'), name='unique_product_info'),
        ),
    ]
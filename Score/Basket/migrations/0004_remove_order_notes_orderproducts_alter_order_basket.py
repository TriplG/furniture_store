# Generated by Django 4.0.1 on 2022-04-24 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Basket', '0003_statusorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='notes',
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basket.product', verbose_name='Товар')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basket.orderproducts', verbose_name='Корзина'),
        ),
    ]
# Generated by Django 4.0.1 on 2022-04-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basket', '0008_alter_statusorder_status_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusorder',
            name='status_name',
            field=models.CharField(max_length=25, verbose_name='Статус'),
        ),
    ]

# Generated by Django 4.2 on 2023-04-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryparameter',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='inventoryparameter',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='value'),
        ),
    ]

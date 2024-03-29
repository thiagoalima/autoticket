# Generated by Django 4.2 on 2023-04-16 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iac', '0002_alter_inventoryparameter_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaybookParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('value', models.TextField(blank=True, null=True, verbose_name='value')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playbookParameters', to='iac.typeinput')),
            ],
        ),
    ]

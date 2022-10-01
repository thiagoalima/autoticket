# Generated by Django 4.0.5 on 2022-10-01 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoticketapp', '0002_alter_ticket_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, null=True, verbose_name='Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, null=True, verbose_name='Serviço')),
                ('status', models.BooleanField(default=False)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoticketapp.group')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, null=True, verbose_name='Equipe')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('codigo', models.TextField(verbose_name='Código')),
                ('service', models.ManyToManyField(to='autoticketapp.service')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoticketapp.team'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-09-24 02:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectpermission',
            name='actions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), help_text='A lista de ações concedidas por esta permissão', size=None),
        ),
        migrations.AlterField(
            model_name='objectpermission',
            name='constraints',
            field=models.JSONField(blank=True, help_text='Filtro do conjunto de consultas que corresponde aos objetos aplicáveis do(s) tipo(s) selecionado(s)', null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='write_enabled',
            field=models.BooleanField(default=True, help_text='Permite criar/atualizar/deletar operações com essa chave'),
        ),
    ]

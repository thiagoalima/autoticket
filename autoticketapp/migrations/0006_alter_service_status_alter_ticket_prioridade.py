# Generated by Django 4.0.5 on 2022-10-01 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoticketapp', '0005_alter_service_grupo_alter_service_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.IntegerField(choices=[(1, 'Ativo'), (2, 'Inativo')], default=1),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='prioridade',
            field=models.IntegerField(choices=[(1, 'Emergencial'), (2, 'Urgente'), (3, 'Alta'), (4, 'Media'), (5, 'Baixa')], default=4),
        ),
    ]

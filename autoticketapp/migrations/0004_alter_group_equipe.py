# Generated by Django 4.0.5 on 2022-10-01 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoticketapp', '0003_group_service_team_template_group_equipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='autoticketapp.team'),
        ),
    ]
from django.db import models

PRIORIDADE_EMERGENCIAL = 'Emergencial'
PRIORIDADE_URGENTE = 'Urgente'
PRIORIDADE_ALTA = 'Alta'
PRIORIDADE_MEDIA = 'Media'
PRIORIDADE_BAIXA = 'Baixa'

PRIORIDADE_CHOICES = [
    (PRIORIDADE_EMERGENCIAL, 1),
    (PRIORIDADE_URGENTE, 2),
    (PRIORIDADE_ALTA, 3),
    (PRIORIDADE_MEDIA, 4),
    (PRIORIDADE_BAIXA, 5),
]

class Ticket (models.Model):

    numero = models.IntegerField(
        null = True,
    )

    titulo = models.CharField(
        max_length=100,
        verbose_name='Name',
    )

    descricao = models.TextField(
        null = True,
        max_length=255,
        verbose_name='Descrição',
    )

    prioridade = models.CharField(
        max_length=50,
        choices=PRIORIDADE_CHOICES,
        default=PRIORIDADE_MEDIA,
    )

    data_inicio = models.DateTimeField(
        auto_now_add=True,
    )

    data_fim = models.DateTimeField(
        null= True,
    )

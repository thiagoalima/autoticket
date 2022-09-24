import binascii
import os

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from .querysets import RestrictedQuerySet
from .constants import *


__all__ = (
    'ObjectPermission',
    'Token',
    'UserConfig',
)


#
# Proxy models for admin
#

class AdminGroup(Group):
    """
    Proxy contrib.auth.models.Group for the admin UI
    """
    class Meta:
        verbose_name = 'Group'
        proxy = True


class AdminUser(User):
    """
    Proxy contrib.auth.models.User for the admin UI
    """
    class Meta:
        verbose_name = 'User'
        proxy = True


#
# REST API
#

class Token(models.Model):
    """
    Um token de API usado para autenticação do usuário. Isso estende o modelo de estoque para permitir que cada usuário tenha vários tokens.
     Ele também suporta a configuração de um tempo de expiração e a alternância da capacidade de gravação.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tokens'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    expires = models.DateTimeField(
        blank=True,
        null=True
    )
    key = models.CharField(
        max_length=40,
        unique=True,
        validators=[MinLengthValidator(40)]
    )
    write_enabled = models.BooleanField(
        default=True,
        help_text='Permite criar/atualizar/deletar operações com essa chave'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        pass

    def __str__(self):
        # Exiba apenas os últimos 24 bits do token para evitar exposição acidental.
        return f"{self.key[-6:]} ({self.user})"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        # Gera uma chave aleatória de 160 bits expressa em hexadecimal.
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def is_expired(self):
        if self.expires is None or timezone.now() < self.expires:
            return False
        return True


#
# Permissions
#

class ObjectPermission(models.Model):
    """
     Um mapeamento de permissão de visualização, adição, alteração e/ou exclusão de usuários e/ou grupos para um conjunto arbitrário de objetos
     identificado por parâmetros de consulta ORM.
     """
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    enabled = models.BooleanField(
        default=True
    )
    object_types = models.ManyToManyField(
        to=ContentType,
        limit_choices_to=OBJECTPERMISSION_OBJECT_TYPES,
        related_name='object_permissions'
    )
    groups = models.ManyToManyField(
        to=Group,
        blank=True,
        related_name='object_permissions'
    )
    users = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='object_permissions'
    )
    actions = ArrayField(
        base_field=models.CharField(max_length=30),
        help_text="A lista de ações concedidas por esta permissão"
    )
    constraints = models.JSONField(
        blank=True,
        null=True,
        help_text="Filtro do conjunto de consultas que corresponde aos objetos aplicáveis do(s) tipo(s) selecionado(s)"
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        verbose_name = "permission"

    def __str__(self):
        return self.name

    def list_constraints(self):
        """
        Retorne todos os conjuntos de restrições como uma lista (mesmo que apenas um único conjunto seja definido).
        """
        if type(self.constraints) is not list:
            return [self.constraints]
        return self.constraints

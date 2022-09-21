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
    An API token used for user authentication. This extends the stock model to allow each user to have multiple tokens.
    It also supports setting an expiration time and toggling write ability.
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
        help_text='Permit create/update/delete operations using this key'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        pass

    def __str__(self):
        # Only display the last 24 bits of the token to avoid accidental exposure.
        return f"{self.key[-6:]} ({self.user})"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        # Generate a random 160-bit key expressed in hexadecimal.
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
    A mapping of view, add, change, and/or delete permission for users and/or groups to an arbitrary set of objects
    identified by ORM query parameters.
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
        help_text="The list of actions granted by this permission"
    )
    constraints = models.JSONField(
        blank=True,
        null=True,
        help_text="Queryset filter matching the applicable objects of the selected type(s)"
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        verbose_name = "permission"

    def __str__(self):
        return self.name

    def list_constraints(self):
        """
        Return all constraint sets as a list (even if only a single set is defined).
        """
        if type(self.constraints) is not list:
            return [self.constraints]
        return self.constraints

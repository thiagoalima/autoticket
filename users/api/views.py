from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.db.models import Count
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from autoticket.users.querysets import RestrictedQuerySet

from users import filtersets
from users.models import ObjectPermission, Token
from . import serializers


class UsersRootView(APIRootView):
    """
    Users API root view
    """
    def get_view_name(self):
        return 'Users'


#
# Users and groups
#

class UserViewSet(ModelViewSet):
    queryset = RestrictedQuerySet(model=User).prefetch_related('groups').order_by('username')
    serializer_class = serializers.UserSerializer
    filterset_class = filtersets.UserFilterSet


class GroupViewSet(ModelViewSet):
    queryset = RestrictedQuerySet(model=Group).annotate(user_count=Count('user')).order_by('name')
    serializer_class = serializers.GroupSerializer
    filterset_class = filtersets.GroupFilterSet


#
# REST API tokens
#

class TokenViewSet(ModelViewSet):
    queryset = RestrictedQuerySet(model=Token).prefetch_related('user')
    serializer_class = serializers.TokenSerializer
    filterset_class = filtersets.TokenFilterSet

    def get_queryset(self):
        """
        Limite os não superusuários aos seus próprios Tokens.
        """
        queryset = super().get_queryset()
        # Workaround for schema generation (drf_yasg)
        if getattr(self, 'swagger_fake_view', False):
            return queryset.none()
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)


class TokenProvisionView(APIView):
    """
    Endpoint da API REST não autenticado por meio do qual um usuário pode criar um Token.
    """
    permission_classes = []

    def post(self, request):
        serializer = serializers.TokenProvisionSerializer(data=request.data)
        serializer.is_valid()

        # Authenticate the user account based on the provided credentials
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        if not username or not password:
            raise AuthenticationFailed("O nome de usuário e a senha devem ser fornecidos para provisionar um token.")
        user = authenticate(request=request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed("username/password Invalido")

        # Create a new Token for the User
        token = Token(user=user)
        token.save()
        data = serializers.TokenSerializer(token, context={'request': request}).data

        return Response(data, status=HTTP_201_CREATED)


#
# ObjectPermissions
#

class ObjectPermissionViewSet(ModelViewSet):
    queryset = ObjectPermission.objects.prefetch_related('object_types', 'groups', 'users')
    serializer_class = serializers.ObjectPermissionSerializer
    filterset_class = filtersets.ObjectPermissionFilterSet

from django.contrib.auth.models import Permission, Group
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True,
        error_messages = {'required': 'Ops, o e-mail é obrigatório!'}

    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        error_messages= { 'required' : 'Senha não informada'}
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            except :
                msg = _('Usuário não encontrado.')
                raise serializers.ValidationError(msg, code='authorization')
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Usuário inválido.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Informe e-mail e senha.".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
    class Meta:
        model = User
        exclude = [
            'password',
        ]


class UserModelSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'telefone', 'data_nascimento', 'password', 'first_name',
                  'last_name', 'is_staff', 'is_superuser', 'is_active', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True}}


class UserEditSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'cpf', 'telefone',
            'data_nascimento', 'is_superuser', 'is_active', 'is_staff', 'is_superuser', 'user_permissions',
            'groups'        ]
        


class CreateUserSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'cpf', 'telefone', 'data_nascimento', 'password', 'first_name',
            'last_name', 'is_staff', 'is_superuser', 'is_active','user_permissions', 'groups'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError("A senha é obrigatória.")
        user_permissions = validated_data.pop('user_permissions', [])
        groups = validated_data.pop('groups', [])
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        user.user_permissions.set(user_permissions)
        user.groups.set(groups)
        
        return user


class UserPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    codename = serializers.CharField()
    action = serializers.ChoiceField(choices=['add', 'remove'])


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        trim_whitespace=False,
        write_only=True,
        error_messages= { 'required' : 'Senha não informada'}
    )
    def validate(self, data):
        user = self.context['request'].user
        if user.password_set:
            msg = _('Senha já foi definida.')
            raise serializers.ValidationError(msg, code='authorization')
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        password = self.validated_data['password']
        user.set_password(password)
        user.password_set = True
        user.save()

        return user
    
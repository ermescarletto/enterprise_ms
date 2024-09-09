
from rest_framework import parsers, renderers, generics, status
from rest_framework.authtoken.models import Token
from .serializers import AuthTokenSerializer, UserSerializer, UserModelSerializer, CreateUserSerializer, UserPermissionSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from .models import *



class AuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(

                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="E-mail válido para autenticação.",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Senha para autenticação.",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user is valid
        if 'user' not in serializer.validated_data:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        # Check if the password is valid
        if not user.check_password(request.data.get('password')):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': user_serializer.data})


class UserListViewAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserCRUDViewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

class ManageUserPerms(APIView):
    queryset = User.objects.all()

    def post(self, request):
        serializer = UserPermissionSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            codename = serializer.validated_data['codename']
            action = serializer.validated_data['action']
            try:
                user = User.objects.get(id=user_id)
                permission = Permission.objects.get(codename=codename)
                print(permission.codename)
                if action == 'add':
                    user.user_permissions.add(permission.codename)
                    return Response({'message' : 'Permissão {} adicionada com sucesso.'.format(permission)})
                elif action == 'remove':
                    user.user_permissions.remove(permission.codename)
                    return Response({'message' : 'Permissão {} removida com sucesso'.format(permission)})
            except User.DoesNotExist:
                return Response({'error' : 'Usuário não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
            except Permission.DoesNotExist:
                return Response({'error' : 'Permissão não encontrada.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = User




obtain_auth_token = AuthToken.as_view()
user_list = UserListViewAPI.as_view()
user_crud = UserCRUDViewAPI().as_view()
user_create = UserCreateView().as_view()
manage_perms = ManageUserPerms.as_view()
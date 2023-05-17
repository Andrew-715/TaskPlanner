from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView
from rest_framework.response import Response

from core.serializers import RegistrationSerializer, LoginSerializer, \
    UpdatePasswordSerializer, UserSerializer

USER_MODEL = get_user_model()

'''
Вью с регистрацией, в которой указываем права доступа к форме
регистрации и указываем необходимый сериалайзер.
'''


class RegistrationView(CreateAPIView):
    model = USER_MODEL
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


'''
Вью для авторизации пользователя.
'''


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    '''
    Переопределяем метод POST.
    Добавляем проверку данных пользователя с базой и 
    авторизуем пользователя.
    '''

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


'''
Вью для получения, обновления и удаления данных пользователя.
'''


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = USER_MODEL.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Вью для обновления пароля.
'''


class UpdatePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user

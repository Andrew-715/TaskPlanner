from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import HiddenField, CurrentUserDefault, CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated

USER_MODEL = get_user_model()

'''Сериализатор для проверки на валидность создания/изменения пароля.'''


class PasswordField(CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


'''Сериализатор для регистрации.'''


class RegistrationSerializer(ModelSerializer):
    '''
    Два поля с паролями, которые должны быть валидными.
    '''
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = USER_MODEL
        read_only_fields = ('id',)
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        )

    '''Проверка на совпадение паролей для авторизации и регистрации.'''

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Password and password_repeat do not match.')
        return attrs

    '''Кеширование пароля при регистрации.'''

    def create(self, validated_data: dict) -> USER_MODEL:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


'''Сериализатор для авторизации.'''


class LoginSerializer(ModelSerializer):
    username = CharField(required=True)
    password = CharField(required=True, write_only=True)

    def create(self, validated_data: dict) -> USER_MODEL:
        '''
        Проверка: данные зарегистрированного пользователя совпадают с
        данными в базе.
        '''
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )):
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = '__all__'


'''Сериализатор для отображения информации пользователю.'''


class UserSerializer(ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


'''Сериализатор для обновления пароля.'''


class UpdatePasswordSerializer(Serializer):
    user = HiddenField(default=CurrentUserDefault())
    old_password = CharField(required=True, write_only=True)
    new_password = CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        '''
        Проверка: передаётся ли пользователь вместе с другими данными.
        '''
        if not (user := attrs['user']):
            raise NotAuthenticated
        '''
        Проверка: совпадает ли введённый старый пароль пользователем
        со старым паролем в базе.
        '''
        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'incorrect password'})
        return attrs

    '''Закрываем доступ к методу 'create'.'''

    def create(self, validated_data: dict) -> USER_MODEL:
        raise NotImplementedError

    '''Кешируем и обновляем пароль.'''

    def update(self, instance: user, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance

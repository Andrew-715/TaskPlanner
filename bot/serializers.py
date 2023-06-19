from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from bot.models import TgUser


class TgUserSerializer(ModelSerializer):
    tg_id = IntegerField(source='chat_id', read_only=True)
    user_id = IntegerField(source='user.id', read_only=True)
    verification_code = CharField(write_only=True)

    def validate_verification_code(self, code: str) -> str:
        try:
            tg_user = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise ValidationError('Invalid verification code')
        else:
            if tg_user.is_verified:
                raise ValidationError('Unsupported error')

            self.instance = tg_user
            return code

    class Meta:
        model = TgUser
        fields = ('tg_id', 'user_id', 'verification_code')

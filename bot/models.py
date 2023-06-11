from django.contrib.auth import get_user_model
from django.db.models import Model, CASCADE, OneToOneField
from django.db.models.fields import BigIntegerField, CharField
from django.utils.crypto import get_random_string

USER = get_user_model()


class TgUser(Model):
    telegram_chat_id = BigIntegerField(
        primary_key=True,
        editable=False,
        unique=True
    )
    telegram_user_id = OneToOneField(
        to=USER,
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    verification_code = CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.__class__.__name__} {self.telegram_chat_id}'

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=['verification_code'])

    @property
    def is_verified(self) -> bool:
        return bool(self.telegram_user_id)

    @staticmethod
    def _generate_verification_code() -> str:
        return get_random_string(20)

    class Meta:
        verbose_name = "Телеграм-пользователь"
        verbose_name_plural = "Телеграм-пользователи"

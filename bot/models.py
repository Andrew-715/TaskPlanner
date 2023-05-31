from django.db import models

from core.models import User


class TgUser(models.Model):
    telegram_chat_id = models.IntegerField()
    telegram_user_id = models.IntegerField()
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

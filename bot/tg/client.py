from typing import Any

import requests
from marshmallow import ValidationError

from TaskPlanner import settings
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token: str | None = None) -> None:
        self.__token = token if token else settings.BOT_TOKEN
        self.__base_url = f"https://api.telegram.org/bot{self.__token}/"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get('getUpdates', offset=offset, timeout=timeout)
        return GetUpdatesResponse.Schema().load(data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text)
        return SendMessageResponse.Schema().load(data)

    def __get_url(self, method: str) -> str:
        return f"{self.__base_url}{method}"

    def _get(self, command: str, **params: Any) -> dict:
        url = self.__get_url(command)
        response = requests.get(url, params=params)
        if not response.ok:
            print(f'Invalid status code from telegram '
                  f'{response.status_code} on command {command}')
        return response.json()


def _serialize_response(serializer_class, data):
    try:
        return serializer_class(**data)
    except ValidationError as e:
        print(f'Failed to serializer telegram response due {e}')
        raise ValueError

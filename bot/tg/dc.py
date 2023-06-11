from dataclasses import dataclass
from typing import List

import marshmallow
import marshmallow_dataclass


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str


@dataclass
class FromMessage:
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


@dataclass
class Message:
    message_id: int
    from_: FromMessage
    chat: Chat
    date: int
    text: str | None


@dataclass
class UpdateObj:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


GetUpdatesSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageSchema = marshmallow_dataclass.class_schema(SendMessageResponse)

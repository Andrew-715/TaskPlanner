from dataclasses import dataclass, field
from typing import List

import marshmallow
import marshmallow_dataclass


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class FromMessageResponse:
    ok: bool
    result: FromMessage  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class ChatResponse:
    ok: bool
    result: Chat  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE

UpdatesSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
FromMessageSchema = marshmallow_dataclass.class_schema(FromMessageResponse)
ChatSchema = marshmallow_dataclass.class_schema(ChatResponse)

from dataclasses import dataclass, field
from typing import Callable, Any

import marshmallow
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


@dataclass
class FSMData:
    next_handler: Callable
    data: dict[str, Any] = field(default_factory=dict)

    class Meta:
        unknown = marshmallow.EXCLUDE


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.clients: dict[int, FSMData] = {}

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started'))
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, _ = TgUser.objects.get_or_create(
            telegram_chat_id=msg.chat.id)

        if tg_user.is_verified:
            self.handle_authorized_user(tg_user, msg)
        else:
            self.handle_unauthorized_user(tg_user, msg)

    def handle_authorized_user(self, tg_user: TgUser, msg: Message) -> None:
        self.tg_client.send_message(tg_user.telegram_chat_id, 'You authorized!')
        if msg.text.startswith('/'):
            if msg.text == '/goals':
                self.handle_goals_command(tg_user, msg)
            elif msg.text == '/create':
                self.handle_create_command(tg_user, msg)
            elif msg.text == '/cancel':
                self.clients.pop(tg_user.telegram_chat_id, None)
                self.tg_client.send_message(tg_user.telegram_chat_id, 'Creation canceled.')
            else:
                self.tg_client.send_message(tg_user.telegram_chat_id, 'Command not found.')
        elif tg_user.telegram_chat_id in self.clients:
            client = self.clients[tg_user.telegram_chat_id]
            client.next_handler(tg_user=tg_user, msg=msg, **client.data)

    def handle_unauthorized_user(self, tg_user: TgUser, msg: Message) -> None:
        self.tg_client.send_message(tg_user.telegram_chat_id, 'Hello, friend!')
        tg_user.update_verification_code()
        self.tg_client.send_message(tg_user.telegram_chat_id,
                                    f'Your verification code: {tg_user.verification_code}')

    def handle_goals_command(self, tg_user: TgUser, msg: Message) -> None:
        goals = Goal.objects.exclude(status=Goal.Status.archived).filter(
            user=tg_user.user)
        if goals:
            text = 'Your goals:\n' + '\n'.join([f'{goal.id} {goal.title}' for goal in goals])
        else:
            text = 'You have not goals'

        self.tg_client.send_message(tg_user.telegram_chat_id, text)

    def handle_create_command(self, tg_user: TgUser, msg: Message) -> None:
        categories = GoalCategory.objects.filter(
            user=tg_user.user).exclude(is_deleted=True)
        if not categories:
            self.tg_client.send_message(
                tg_user.telegram_chat_id, 'You have not categories')
            return

        text = 'Select cat to create goals:\n' \
               + '\n'.join([f'{cat.id} {cat.title}' for cat in categories])
        self.tg_client.send_message(tg_user.telegram_chat_id, text)
        self.clients[tg_user.telegram_chat_id] = FSMData(next_handler=self._get_category)

    def _get_category(self, tg_user: TgUser, msg: Message, **kwargs) -> None:
        try:
            category = GoalCategory.objects.get(pk=msg.text)
        except GoalCategory.DoesNotExist:
            self.tg_client.send_message(tg_user.telegram_chat_id, 'Category not exists')
            return
        else:
            self.clients[tg_user.telegram_chat_id].next_handler = self._create_goal
            self.clients[tg_user.telegram_chat_id].data['category'] = category
            self.tg_client.send_message(tg_user.telegram_chat_id, 'Set goal title')

    def _create_goal(self, tg_user: TgUser, msg: Message, **kwargs) -> None:
        category = kwargs['category']
        Goal.objects.create(
            category=category, user=tg_user.user, title=msg.text)
        self.tg_client.send_message(tg_user.telegram_chat_id, 'New goal create')
        self.clients.pop(tg_user.telegram_chat_id, None)

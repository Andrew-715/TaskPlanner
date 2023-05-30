from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault, ChoiceField
from rest_framework.relations import SlugRelatedField
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from core.models import User
from goals.models import Board, BoardParticipant


class BoardCreateSerializer(ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"


class BoardParticipantSerializer(ModelSerializer):
    role = ChoiceField(required=True, choices=BoardParticipant.editable_roles)
    user = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    '''
    Проверка: 'владелец' не сможет изменить себе роль на 
    'читатель' или 'редактор'.
    '''

    def validate_user(self, user: User) -> User:
        if self.context['request'].user == user:
            raise ValidationError('Failed to change your role')
        return user

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(BoardCreateSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        request: Request = self.context['request']

        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=request.user).delete()
            BoardParticipant.objects.bulk_create(
                [
                    BoardParticipant(
                        user=participants['user'],
                        role=participants['role'],
                        board=instance
                    )
                    for participants in validated_data.get('participants', [])
                ],
                ignore_conflicts=True,
            )

            if title := validated_data.get('title'):
                instance.title = title

            instance.save()

        return instance

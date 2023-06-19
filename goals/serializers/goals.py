from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, BoardParticipant


class GoalSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    '''
    Проверка, что категория создаваемой цели
    принадлежит пользователю.
    '''

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context['request'].user
        ).exists():
            raise PermissionDenied('must be owner or writer in project')

        return value


class GoalUserSerializer(GoalSerializer):
    user = UserSerializer(read_only=True)

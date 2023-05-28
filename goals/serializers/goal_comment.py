from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from goals.models import Goal, GoalComment, BoardParticipant


class CommentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    '''
    Проверка, что комментарий нельзя оставить 
    под удалённой целью.
    '''

    def validate_comment(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError("Goal not found")

        if not BoardParticipant.objects.filter(
                board_id=value.category.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context['request'].user
        ).exists():
            raise PermissionDenied

        return value


class GoalCommentSerializer(CommentSerializer):
    user = UserSerializer(read_only=True)
    goal = PrimaryKeyRelatedField(read_only=True)

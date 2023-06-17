from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from goals.models import GoalCategory, Board, BoardParticipant


class GoalCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    board = None

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError('Board is deleted')

        if not BoardParticipant.objects.filter(
                board_id=board.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context['request'].user
        ).exists():
            raise PermissionDenied

        return board

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCategorySerializer(GoalCreateSerializer):
    user = UserSerializer(read_only=True)

from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment


class GoalCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCategorySerializer(GoalCreateSerializer):
    user = UserSerializer(read_only=True)


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

    def validate_goal(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")

        if value.user_id != self.context["request"].user.id:
            raise PermissionDenied("not owner of category")
        return value

class GoalUserSerializer(GoalSerializer):
    user = UserSerializer(read_only=True)


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

        if value.user_id != self.context["request"].user.id:
            raise PermissionDenied("not owner of category")
        return value


class GoalCommentSerializer(CommentSerializer):
    user = UserSerializer(read_only=True)
    goal = PrimaryKeyRelatedField(read_only=True)

from django.db import transaction
from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal
from goals.permissions import GoalCategoryPermission, BoardPermissions
from goals.serializers.goal_category import GoalCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = GoalCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields = ['title', 'created', 'board']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]
    queryset = GoalCategory.objects.exclude(is_deleted=True)

    '''
    Переопределяем метод 'perform_destroy', чтобы
    категория не удалялась при вызове 'delete'.
    '''

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
            instance.goal_set.update(status=Goal.Status.archived)

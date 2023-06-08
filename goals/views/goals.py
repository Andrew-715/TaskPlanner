from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalFilter
from goals.models import Goal
from goals.permissions import GoalPermission, BoardPermissions
from goals.serializers.goals import GoalSerializer, GoalUserSerializer


class GoalCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer


class GoalListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalUserSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter
    ]
    filterset_class = GoalFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermission, BoardPermissions]
    serializer_class = GoalUserSerializer
    queryset = Goal.objects.exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = Goal.Status.archived
        instance.save(update_fields=['status'])

from django.db import transaction
from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalFilter
from goals.models import Board, Goal, BoardParticipant
from goals.permissions import BoardPermissions
from goals.serializers.board import BoardCreateSerializer, BoardSerializer


class BoardCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer: BoardCreateSerializer) -> None:
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(
                user=self.request.user,
                board=board,
                role=BoardParticipant.Role.owner
            )


class BoardListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer
    filter_backends = [OrderingFilter]
    filterset_class = GoalFilter
    ordering = ['title']

    def get_queryset(self) -> QuerySet(Board):
        return Board.objects.filter(
            participants__user=self.request.user).exclude(is_deleted=True)


class BoardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer
    queryset = Board.objects.prefetch_related(
        'participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )

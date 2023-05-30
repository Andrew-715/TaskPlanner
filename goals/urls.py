from django.urls import path

from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goals import GoalCreateView, GoalListView, GoalView
from goals.views.goal_comment import GoalCommentCreateView, GoalCommentListView, GoalCommentView
from goals.views.board import BoardView, BoardCreateView, BoardListView

urlpatterns = [
    # Board
    path("board/create", BoardCreateView.as_view(), name='board_create'),
    path("board/list", BoardListView.as_view(), name='board_list'),
    path("board/<int:pk>", BoardView.as_view(), name='board_detail'),
    # Category
    path("goal_category/create", GoalCategoryCreateView.as_view(), name='category_create'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='category_list'),
    path("goal_category/<int:pk>", GoalCategoryView.as_view(), name='category_detail'),
    # Goals
    path("goal/create", GoalCreateView.as_view(), name='goal_create'),
    path("goal/list", GoalListView.as_view(), name='goal_list'),
    path("goal/<int:pk>", GoalView.as_view(), name='goal_detail'),
    # Comment
    path("goal_category/create", GoalCommentCreateView.as_view(), name='comment_create'),
    path("goal_category/list", GoalCommentListView.as_view(), name='comment_list'),
    path("goal_category/<int:pk>", GoalCommentView.as_view(), name='comment_detail'),
]

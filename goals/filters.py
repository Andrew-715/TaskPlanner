from django_filters.rest_framework import FilterSet

from goals.models import Goal

'''Фильтрация по: дате дедлайна(от/до), категории, статусу, приоритету.'''


class GoalFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ["lte", "gte"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

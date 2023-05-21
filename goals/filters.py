import django_filters
from django.db import models
from django_filters.rest_framework import FilterSet

from goals.models import Goal

'''
Фильтрация по:
категории/категориям,
приоритету/приоритетам,
дате дедлайна(от/до).
'''


class GoalFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ["lte", "gte"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

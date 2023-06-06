from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFilter

from todo_app.models import Task


class TaskFilterSet(filters.FilterSet):
    created = DateFilter(field_name="created", lookup_expr="date")

    class Meta:
        model = Task
        fields = ["done", "name", "created"]

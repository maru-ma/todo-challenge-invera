from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFilter

from todo_app.models import Task


class TaskFilterSet(filters.FilterSet):
    """
    Filter set for filtering tasks based on specific criteria.

    This filter set allows filtering tasks based on the following fields:
    - done: Filters tasks based on whether they are marked as done or not.
    - name: Filters tasks based on a partial match of the task name.
    - created: Filters tasks based on the date of creation.

    Example usage: /api/todo-lists/{list_id}/tasks/filter?done=true&name=example&created=2023-05-01

    Note: The `created` field supports date filtering using lookup expressions like `date`, `lte`, `gte`, etc.
    """

    created = DateFilter(field_name="created", lookup_expr="date")
    done = filters.BooleanFilter(field_name="done")

    class Meta:
        model = Task
        fields = ["done", "name", "created"]

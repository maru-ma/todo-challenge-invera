from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from todo_app.models import Task

from ..filtersets import TaskFilterSet
from ..pagination import LargerResultsSetPagination
from ..permissions import AllTasksTodoListOwnerOnly, TaskTodoListOwnerOnly
from ..serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Get or create tasks for a specific todo list, ordered by done status.
    """

    serializer_class = TaskSerializer
    permission_classes = [AllTasksTodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(todo_list=self.kwargs["todo_list_pk"]).order_by("done")


class FilterTask(generics.ListAPIView):
    """
    Filter tasks by done status, name, or date of creation for a specific todo list.
    """

    serializer_class = TaskSerializer
    permission_classes = [TaskTodoListOwnerOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"done": ["exact"], "name": ["icontains"]}
    search_fields = ["name", "done"]
    filterset_class = TaskFilterSet

    def get_queryset(self):
        return Task.objects.filter(todo_list=self.kwargs["todo_list_pk"])

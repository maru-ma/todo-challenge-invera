from django_filters.rest_framework import DateFilter, DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics

from todo_app.models import Task, TodoList

from .filtersets import TaskFilterSet
from .pagination import LargerResultsSetPagination
from .permissions import (
    AllTasksTodoListOwnerOnly,
    TaskTodoListOwnerOnly,
    TodoListOwnerOnly,
)
from .serializers import TaskSerializer, TodoListSerializer


@extend_schema(description="Returns the list of all todo lists user is a owner of.")
class ListAddTodoList(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("-updated")


@extend_schema(description="Returns the detail of a todo list.")
class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]


@extend_schema(
    description="Returns the list of the task for the given list ordered by done status. Owner can add taks to the list."
)
class ListAddTask(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AllTasksTodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        return Task.objects.filter(todo_list=todo_list_pk).order_by("done")


@extend_schema(description="Returns the task for the given id.")
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskTodoListOwnerOnly]
    lookup_url_kwarg = "task_pk"


@extend_schema(description="Filters list by archived status and/or name from the lists of the auth user.")
class FilterTodoList(generics.ListAPIView):
    serializer_class = TodoListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"archived": ["exact"], "name": ["icontains"]}
    search_fields = ["name"]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user)


@extend_schema(description="Filter tasks for done status, name or date of creation.")
class FilterTask(generics.ListAPIView):
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"done": ["exact"], "name": ["icontains"]}
    search_fields = ["name"]
    filterset_class = TaskFilterSet

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        return Task.objects.filter(todo_list=todo_list_pk)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from todo_app.models import Task, TodoList

from .pagination import LargerResultsSetPagination
from .permissions import AllTasksTodoListOwnerOnly, TaskTodoListOwnerOnly, TodoListOwnerOnly
from .serializers import TaskSerializer, TodoListSerializer


class ListAddTodoList(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("-updated")


class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]


class ListAddTask(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AllTasksTodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        return Task.objects.filter(todo_list=todo_list_pk).order_by("done")


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskTodoListOwnerOnly]
    lookup_url_kwarg = "task_pk"


class FilterTodoList(generics.ListAPIView):
    serializer_class = TodoListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"archived": ["exact"], "name": ["icontains"]}
    search_fields = ["name"]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user)


class FilterTask(generics.ListAPIView):
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"done": ["exact"], "name": ["icontains"]}
    search_fields = ["name"]

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        return Task.objects.filter(todo_list=todo_list_pk)

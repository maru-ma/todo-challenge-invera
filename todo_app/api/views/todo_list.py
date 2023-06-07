from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from todo_app.models import TodoList

from ..pagination import LargerResultsSetPagination
from ..permissions import TodoListOwnerOnly
from ..serializers import TodoListSerializer


class ListAddTodoListView(generics.ListCreateAPIView):
    """
    Get or create todo lists owned by the authenticated user.
    """

    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("-updated")


class TodoListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a specific todo list.
    """

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]


class FilterTodoList(generics.ListAPIView):
    """
    Filter todo lists by archived status and/or name for the authenticated user.
    """

    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"archived": ["exact"], "name": ["icontains"]}
    search_fields = ["name"]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user)

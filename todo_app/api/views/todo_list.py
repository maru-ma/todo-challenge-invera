from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, generics
from todo_app.models import TodoList

from ..pagination import LargerResultsSetPagination
from ..permissions import TodoListOwnerOnly
from ..serializers import TodoListSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    """
    CRUD for todo lists owned by the authenticated user.
    """

    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return TodoList.objects.all().order_by("-updated")

        return TodoList.objects.filter(owner=user).order_by("-updated")

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class FilterTodoList(generics.ListAPIView):
    """
    Filter todo lists by archived status and/or name for the authenticated user.
    """

    serializer_class = TodoListSerializer
    permission_classes = [TodoListOwnerOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"archived": ["exact"], "name": ["exact"]}
    search_fields = ["name"]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user)

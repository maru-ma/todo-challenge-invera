from rest_framework import generics

from .pagination import LargerResultsSetPagination
from .permissions import AllItemsTodoListOwnerOnly, TodoListOwnerOnly, ItemTodoListOwnerOnly
from .serializers import ItemSerializer, TodoListSerializer
from todo_app.models import Item, TodoList


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


class ListAddItem(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllItemsTodoListOwnerOnly]
    pagination_class = LargerResultsSetPagination

    def get_queryset(self):
        todo_list_pk = self.kwargs["pk"]
        return Item.objects.filter(todo_list=todo_list_pk).order_by("done")


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [ItemTodoListOwnerOnly]
    lookup_url_kwarg = "item_pk"
